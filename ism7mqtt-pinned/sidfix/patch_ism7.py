#!/usr/bin/env python3
"""Patch Ism7Client for WolfLink 300.x XML issues and header/body type mismatches."""

from pathlib import Path
import re

PATH = Path("/src/src/ism7mqtt/ISM7/Ism7Client.cs")
text = PATH.read_text(encoding="utf-8")

HELPERS = """
        private static string SanitizeXmlChars(string xml)
        {
            var sb = new StringBuilder(xml.Length);
            foreach (var c in xml)
            {
                if (c >= 0x20 || c == '\\t' || c == '\\n' || c == '\\r')
                    sb.Append(c);
            }
            return sb.ToString();
        }

        private static PayloadType ResolveXmlPayloadType(PayloadType headerType, string xml)
        {
            if (xml.Contains("direct-logon-response", StringComparison.Ordinal))
                return PayloadType.DirectLogonResp;
            if (xml.Contains("<tbres", StringComparison.Ordinal))
                return PayloadType.TgrBundleResp;
            if (xml.Contains("read-systemconfig-response", StringComparison.Ordinal)
                || xml.Contains("systemconfig-response", StringComparison.Ordinal))
                return PayloadType.SystemconfigResp;
            return headerType;
        }

        private IResponse DeserializeXml(PayloadType headerType, Stream data)
        {
            using var ms = new MemoryStream();
            data.CopyTo(ms);
            var xml = SanitizeXmlChars(Encoding.UTF8.GetString(ms.ToArray()));
            var type = ResolveXmlPayloadType(headerType, xml);
            using var clean = new MemoryStream(Encoding.UTF8.GetBytes(xml));
            return type switch
            {
                PayloadType.DirectLogonResp => (IResponse)GetSerializer<LoginResp>().Deserialize(clean),
                PayloadType.SystemconfigResp => (IResponse)GetSerializer<SystemconfigResp>().Deserialize(clean),
                PayloadType.TgrBundleResp => (IResponse)GetSerializer<TelegramBundleResp>().Deserialize(clean),
                _ => throw new ArgumentOutOfRangeException(nameof(headerType), headerType,
                    $"Unexpected XML: {xml[..Math.Min(80, xml.Length)]}")
            };
        }
"""

# Replace existing patched Deserialize or original
pat = re.compile(
    r"        private IResponse Deserialize\(PayloadType type, Stream data\)\s*\{.*?^        \}",
    re.MULTILINE | re.DOTALL,
)

NEW_DESERIALIZE = """        private IResponse Deserialize(PayloadType type, Stream data)
        {
            switch (type)
            {
                case PayloadType.DirectLogonResp:
                case PayloadType.SystemconfigResp:
                case PayloadType.TgrBundleResp:
                    return DeserializeXml(type, data);
                case PayloadType.KeepAlive:
                    using (var reader = new BinaryReader(data))
                    {
                        var buffer = reader.ReadBytes(2);
                        return new KeepAliveResp(BinaryPrimitives.ReadInt16BigEndian(buffer));
                    }
                default:
                    throw new ArgumentOutOfRangeException(nameof(type), type, "unsupported payload type");
            }
        }"""

# Remove old helper blocks we may have added earlier
for old in (
    "SanitizeXmlStream",
    "ResolveXmlPayloadType",
    "DeserializeXml",
):
    pass

# Strip prior patch helpers (between GetSerializer and Deserialize, or before Deserialize)
text = re.sub(
    r"\n        private static Stream SanitizeXmlStream.*?(?=\n        private IResponse Deserialize)",
    "\n",
    text,
    flags=re.DOTALL,
)
text = re.sub(
    r"\n        private static string SanitizeLogonXml.*?(?=\n        private IResponse Deserialize)",
    "\n",
    text,
    flags=re.DOTALL,
)
text = re.sub(
    r"\n        private static string SanitizeXmlChars.*?(?=\n        private (IResponse Deserialize|XmlSerializer GetSerializer))",
    "\n",
    text,
    flags=re.DOTALL,
)
text = re.sub(
    r"\n        private static PayloadType ResolveXmlPayloadType.*?(?=\n        private (IResponse Deserialize|XmlSerializer GetSerializer))",
    "\n",
    text,
    flags=re.DOTALL,
)
text = re.sub(
    r"\n        private static IResponse DeserializeXml.*?(?=\n        private (IResponse Deserialize|XmlSerializer GetSerializer))",
    "\n",
    text,
    flags=re.DOTALL,
)

m = pat.search(text)
if not m:
    raise SystemExit("Deserialize method not found in Ism7Client.cs")

text = pat.sub(NEW_DESERIALIZE, text, count=1)

anchor = "        private IResponse Deserialize(PayloadType type, Stream data)"
if "ResolveXmlPayloadType" not in text:
    text = text.replace(anchor, HELPERS + "\n" + anchor, 1)

PATH.write_text(text, encoding="utf-8")
print("Patched", PATH)
