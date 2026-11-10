//! Desktop implementation of the optional Material Community lookup plugin.
use soar_app::host::{Host, ModuleBuilder, NativeModule, RegisterError, Value};
const GLYPHS: &str = include_str!("../assets/glyphmap.txt");
fn glyph(name: &str) -> String {
    if name.is_empty() { return String::new(); }
    let mut low = 0;
    let mut high = GLYPHS.len();
    while low < high {
        let middle = low + (high - low) / 2;
        let start = GLYPHS[..middle].rfind('\n').map_or(0, |i| i + 1);
        let end = GLYPHS[middle..].find('\n').map_or(GLYPHS.len(), |i| middle + i);
        let Some((key, code)) = GLYPHS[start..end].split_once('\t') else { return "?".into() };
        match key.cmp(name) {
            std::cmp::Ordering::Less => low = end + 1,
            std::cmp::Ordering::Greater => high = start,
            std::cmp::Ordering::Equal => return u32::from_str_radix(code, 16).ok().and_then(char::from_u32).unwrap_or('?').to_string(),
        }
    }
    "?".into()
}
struct MaterialIcons;
impl NativeModule for MaterialIcons {
    fn name(&self) -> &str { "materialCommunityIcons" }
    fn register(&self, m: &mut ModuleBuilder<'_>) -> Result<(), RegisterError> {
        m.sync("glyph(name: string): string", |args| Ok(Value::Str(glyph(args.first().and_then(Value::as_str).unwrap_or_default()))))?;
        Ok(())
    }
}
pub fn register(host: &mut Host) { host.add(&MaterialIcons).expect("material icon plugin signatures"); }
#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn lookup_matches_map_and_fallbacks() {
        for line in GLYPHS.lines() {
            let (name, hex) = line.split_once('\t').unwrap();
            assert_eq!(glyph(name), char::from_u32(u32::from_str_radix(hex, 16).unwrap()).unwrap().to_string());
        }
        assert_eq!(glyph(""), ""); assert_eq!(glyph("not-an-icon"), "?"); assert_eq!(glyph("☃"), "?");
    }
}
