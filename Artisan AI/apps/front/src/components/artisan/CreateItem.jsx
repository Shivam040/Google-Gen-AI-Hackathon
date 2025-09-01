// front/src/components/artisan/CreateItem.jsx
import { useRef, useState, useMemo } from "react";
import Button from "../ui/Button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { ArrowLeft, Plus, Upload, Camera, Wand2, Sparkles, Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8080";
const PLACEHOLDER = "/placeholder-640x360.png";
const DEFAULT_CURRENCY = "INR";
const CURRENCIES = ["INR", "USD", "EUR"];

const THEMES = ["Traditional", "Modern", "Festival", "Minimal", "Heritage", "Fusion"];
const PRODUCT_TYPES = {
  Art: ["Drawing", "Painting", "Calligraphy"],
  "Craft Objects": ["Pottery", "Woodwork", "Metalwork"],
  Textiles: ["Clothing", "Weaving", "Embroidery"],
  Accessories: ["Jewelry", "Bags", "Home Decor"],
};
const TONES = ["Professional", "Friendly", "Playful", "Narrative", "Persuasive", "Empathetic", "Luxury", "Minimal", "Gen Z / Casual"];
const LANGS = [
  ["en", "English"],
  ["hi", "हिन्दी"],
  ["bn", "বাংলা"],
  ["mr", "मराठी"],
  ["te", "తెలుగు"],
  ["ta", "தமிழ்"],
];

/* ------------ Pretty field primitives (floating labels) ------------ */
const baseField =
  "peer w-full rounded-xl bg-slate-800/70 border border-slate-700 text-slate-100 " +
  "px-3 pt-5 pb-2 h-12 shadow-inner outline-none " +
  "placeholder-transparent focus:ring-2 focus:ring-sky-500/60 focus:border-sky-500/60";

const labelFloat =
  "pointer-events-none absolute left-3 top-2 text-xs text-slate-400 transition-all " +
  "peer-focus:text-sky-300 peer-focus:top-2 peer-focus:text-xs " +
  "peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-sm peer-placeholder-shown:text-slate-500";

const numberFix =
  "[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none";

function FloatInput({ label, type = "text", value, onChange, className = "", ...rest }) {
  return (
    <div className="relative">
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder=" "
        className={`${baseField} ${type === "number" ? numberFix : ""} ${className}`}
        autoComplete="off"
        {...rest}
      />
      <label className={labelFloat}>{label}</label>
    </div>
  );
}

function FloatTextarea({ label, value, onChange, rows = 4, className = "", ...rest }) {
  return (
    <div className="relative">
      <textarea
        rows={rows}
        value={value}
        onChange={onChange}
        placeholder=" "
        className={`peer w-full rounded-xl bg-slate-800/70 border border-slate-700 text-slate-100 px-3 pt-6 pb-3 shadow-inner outline-none focus:ring-2 focus:ring-sky-500/60 focus:border-sky-500/60 ${className}`}
        {...rest}
      />
      <label className="pointer-events-none absolute left-3 top-2.5 text-xs text-slate-400 transition-all peer-focus:text-sky-300">
        {label}
      </label>
    </div>
  );
}

function LabeledSelect({ label, value, onChange, children }) {
  return (
    <div>
      <div className="mb-1 text-xs text-slate-400">{label}</div>
      <select
        value={value}
        onChange={onChange}
        className="w-full h-12 rounded-xl bg-slate-800/70 border border-slate-700 text-slate-100 px-3 shadow-inner outline-none focus:ring-2 focus:ring-sky-500/60 focus:border-sky-500/60"
      >
        {children}
      </select>
    </div>
  );
}

/* -------------------------- Small KV editor ------------------------- */
function KVEditor({ title, rows, setRows }) {
  const add = () => setRows((r) => [...r, { k: "", v: "" }]);
  const update = (i, key, val) => setRows((r) => r.map((row, idx) => (idx === i ? { ...row, [key]: val } : row)));
  const remove = (i) => setRows((r) => r.filter((_, idx) => idx !== i));

  return (
    <Card className="bg-slate-900/60 border border-slate-700/60">
      <CardHeader className="flex-row items-center justify-between">
        <CardTitle className="text-slate-100">{title}</CardTitle>
        <Button size="sm" variant="secondary" onClick={add}>Add</Button>
      </CardHeader>
      <CardContent className="space-y-2">
        {rows.length === 0 ? <div className="text-sm text-slate-400">No entries yet.</div> : null}
        {rows.map((r, i) => (
          <div key={i} className="grid grid-cols-12 gap-2">
            <FloatInput label="Key" value={r.k} onChange={(e) => update(i, "k", e.target.value)} className="col-span-5" />
            <FloatInput label="Value" value={r.v} onChange={(e) => update(i, "v", e.target.value)} className="col-span-6" />
            <Button size="sm" variant="destructive" className="col-span-1" onClick={() => remove(i)}>Remove</Button>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

/* ------------------------------- Page ------------------------------- */
export default function CreateItem({ onClose, onCreate, mode = "page" }) {
  const [name, setName] = useState("");
  const [theme, setTheme] = useState(THEMES[0]);
  const [ptype, setPtype] = useState("Drawing");
  const [tone, setTone] = useState(TONES[0]);
  const [lang, setLang] = useState("en");

  const [region, setRegion] = useState("");
  const [artisan, setArtisan] = useState("");
  const [price, setPrice] = useState(0);
  const [currency, setCurrency] = useState(DEFAULT_CURRENCY);
  const [inventory, setInventory] = useState(1);

  const [preview, setPreview] = useState("");
  const [imageDataUrl, setImageDataUrl] = useState("");
  const [imageURL, setImageURL] = useState("");
  const imgRef = useRef(null);

  const [desc, setDesc] = useState("");
  const [story, setStory] = useState("");
  const [post, setPost] = useState("");
  const [imageUrls, setImageUrls] = useState([]);

  const [attrs, setAttrs] = useState([]);
  const [prov, setProv] = useState([]);

  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const primaryBtn =
    "rounded-xl bg-gradient-to-r from-sky-600 to-cyan-500 text-white hover:from-sky-500 hover:to-cyan-400 disabled:opacity-60 disabled:cursor-not-allowed";
  const outlineBtn =
    "rounded-xl border-slate-700 text-slate-200 hover:bg-slate-800/60 hover:border-sky-500/50";

  const slug = (s) =>
    s.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "") || `item-${Date.now()}`;

  async function jsonFetch(path, init) {
    const res = await fetch(`${BASE}${path}`, {
      headers: { "content-type": "application/json", ...(init?.headers || {}) },
      ...init,
    });
    const txt = await res.text();
    const isJSON = (res.headers.get("content-type") || "").includes("application/json");
    const body = isJSON && txt ? JSON.parse(txt) : txt || null;
    if (!res.ok) {
      let msg = body?.detail || body?.message || `${res.status} ${res.statusText}`;
      if (typeof msg === "object") msg = JSON.stringify(msg);
      throw new Error(String(msg));
    }
    return body;
  }

  async function uploadToGCS(file) {
    const q = new URLSearchParams({ filename: file.name, contentType: file.type || "application/octet-stream" });
    const meta = await jsonFetch(`/v1/uploads/signed-url?${q.toString()}`);
    if (meta.upload_url) {
      const put = await fetch(meta.upload_url, {
        method: "PUT",
        headers: { "Content-Type": file.type || "application/octet-stream" },
        body: file,
      });
      if (!put.ok) throw new Error(`Upload failed: ${put.status} ${put.statusText}`);
    }
    return meta.public_url;
  }

  const primaryImage = useMemo(() => {
    if (imageURL) return imageURL;
    if (imageDataUrl?.startsWith("data:")) return imageDataUrl;
    return PLACEHOLDER;
  }, [imageURL, imageDataUrl]);

  const handleFile = async (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setPreview(URL.createObjectURL(f));
    setErr("");
    try {
      setBusy(true);
      const url = await uploadToGCS(f);
      setImageURL(url);
      setImageDataUrl("");
    } catch (error) {
      const reader = new FileReader();
      reader.onload = () => setImageDataUrl(String(reader.result || ""));
      reader.readAsDataURL(f);
      setErr(String(error?.message || error));
    } finally {
      setBusy(false);
    }
  };

  const kvToObject = (rows) =>
    rows.reduce((o, { k, v }) => {
      if (String(k || "").trim()) o[k] = v;
      return o;
    }, {});

  const getAttrObj = () => kvToObject(attrs);
  const getProvObj = () => kvToObject(prov);

  function composeQuickHistory() {
    const title = (name || "Untitled Piece").trim();
    const style = theme?.toLowerCase();
    const type  = ptype?.toLowerCase();
    const where = region?.trim();
    const who   = artisan?.trim();

    const attr = getAttrObj();   // { size, color, technique, material, ... }
    const prov = getProvObj();   // { year, origin, inspiration, care, ... }

    const year      = prov.year || prov.date || prov.made || "";
    const technique = attr.technique || prov.technique || "";
    const material  = attr.material || prov.material || "";
    const size      = attr.size || attr.dimensions || "";
    const color     = attr.color || "";

    // 1) opener sentence
    const opener =
      `"${title}" is a ${[style, type].filter(Boolean).join(" ")} ` +
      `crafted ${who ? `by ${who} ` : ""}${where ? `in ${where} ` : ""}${year ? `in ${year} ` : ""}`
        .replace(/\s+/g, " ")
        .trim() + ".";

    // 2) compact facts line
    const facts = [
      technique && `Technique: ${technique}`,
      material  && `Materials: ${material}`,
      size      && `Size: ${size}`,
      color     && `Palette: ${color}`,
      prov.origin && `Origin: ${prov.origin}`,
      prov.inspiration && `Inspiration: ${prov.inspiration}`,
    ].filter(Boolean).join(" • ");

    // 3) care (optional)
    const care = prov.care || attr.care;

    return [opener, facts && facts + ".", care && `Care: ${care}.`].filter(Boolean).join(" ");
  }

  const genDescQuickHistory = async () => {
    setBusy(true); setErr("");
    try {
      const id = slug(name || "Untitled");
      const patch = buildProductPayload({ id }); // what user filled so far

      // never send UI placeholder
      if (patch.images) {
        patch.images = patch.images.filter((u) => typeof u === "string" && !u.startsWith("/placeholder-"));
        if (patch.images.length === 0) delete patch.images;
      }

      const res = await jsonFetch(`/v1/products/${id}/quicktext`, {
        method: "POST",
        body: JSON.stringify({ patch, mode: "both", persist: false }),
      });

      if (res.description) setDesc(res.description);
      if (res.story) setStory(res.story);
    } catch (e) {
      setErr(String(e?.message || e || "Quick text failed"));
    } finally {
      setBusy(false);
    }
  };




  function buildProductPayload({ id }) {   // Only send real image URLs (GCS) or data URLs. Never send the UI placeholder.
    const images = [];
    if (imageURL) images.push(imageURL);                // https://storage.googleapis.com/...
    else if (imageDataUrl?.startsWith("data:")) images.push(imageDataUrl); // backend will ingest

    return {
      id,
      title: name || "Untitled",
      category: ptype,
      materials: theme ? [theme] : [],
      images,                                           // [] is fine; backend adds its own placeholder
      inventory: Number.isFinite(+inventory) ? +inventory : 1,
      is_active: true,
      price: Number.isFinite(+price) ? +price : 0,
      currency,
      description: desc || undefined,
      region: region || undefined,
      artisan_name: artisan || undefined,
      attributes: kvToObject(attrs),
      provenance: kvToObject(prov),
    };
  }

  const genDesc = async () => {
    setBusy(true); setErr("");
    try {
      const line = `${name || "Untitled"} — ${theme} ${ptype}. Thoughtfully crafted with love.`;
      setDesc((d) => (d ? d + "\n" : "") + line);
    } catch (e) {
      setErr(String(e?.message || e || "Description failed"));
    } finally {
      setBusy(false);
    }
  };

  const genStory = async () => {
    setBusy(true); setErr(""); setStory("");
    try {
      const id = slug(name || "Untitled");
      const payload = buildProductPayload({ id });
            // hard guard: never send the UI placeholder
      if (payload.images) {
        payload.images = payload.images.filter(
          (u) => typeof u === "string" && !u.startsWith("/placeholder-")
        );
        if (payload.images.length === 0) delete payload.images; // omit when empty
      }
      console.log("POST /v1/products payload.images =", payload.images);
      await jsonFetch(`/v1/products/${id}`, { method: "POST", body: JSON.stringify(payload) });
      const gen = await jsonFetch(`/v1/products/${id}/generate`, { method: "POST", body: JSON.stringify({ langs: [lang], tone }) });
      const first = (gen.items || [])[0] || {};
      setStory(first.text || first.gcs_uri || "Generated (stub).");
    } catch (e) {
      setErr(String(e?.message || e || "Story generation failed"));
      setStory((s) => (s ? s + "\n" : "") + `[Story failed] ${String(e?.message || e || "")}`);
    } finally { setBusy(false); }
  };

  const genMarketing = async () => {
    setBusy(true); setErr(""); setPost(""); setImageUrls([]);
    try {
      const id = slug(name || "Untitled");
      const payload = buildProductPayload({ id });
      // hard guard: never send the UI placeholder
      if (payload.images) {
        payload.images = payload.images.filter(
          (u) => typeof u === "string" && !u.startsWith("/placeholder-")
        );
        if (payload.images.length === 0) delete payload.images; // omit when empty
      }
      console.log("POST /v1/products payload.images =", payload.images);
      await jsonFetch(`/v1/products/${id}`, { method: "POST", body: JSON.stringify(payload) });
      const sug = await jsonFetch(`/v1/marketing/suggest?product_id=${encodeURIComponent(id)}&channel=instagram&lang=${encodeURIComponent(lang)}`);
      const tags = Array.isArray(sug.hashtags) ? sug.hashtags.map((t) => String(t).replace(/^#/, "")) : [];
      const created = await jsonFetch(
        `/v1/marketing/${encodeURIComponent(id)}/post?channel=instagram&lang=${encodeURIComponent(lang)}&tone=${encodeURIComponent(tone)}`,
        { method: "POST", body: JSON.stringify(tags) }
      );
      const item = created.item || created || {};
      setPost(item.post_text || item.text || "Post created.");
      if (item.image_uri) setImageUrls([item.image_uri]);
    } catch (e) {
      setErr(String(e?.message || e || "Marketing generation failed"));
      setPost((p) => (p ? p + "\n" : "") + `[Marketing failed] ${String(e?.message || e || "")}`);
    } finally { setBusy(false); }
  };


  /* ---------------------------- Main form ---------------------------- */
  const Content = (
    <div className="grid grid-cols-12 gap-6">
      {/* LEFT */}
      <div className="col-span-12 lg:col-span-4 space-y-4">
        <Card className="bg-slate-900/60 border border-slate-700/60">
          <CardHeader><CardTitle className="text-slate-100">Product Image</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center gap-3">
              <input type="file" accept="image/*" ref={imgRef} onChange={handleFile} className="hidden" />
              <Button variant="outline" onClick={() => imgRef.current?.click()} className={outlineBtn} disabled={busy}>
                <Upload className="h-4 w-4 mr-1" /> Upload
              </Button>
              <span className="text-sm text-slate-400">{preview ? "Selected" : "No file chosen"}</span>
            </div>
            {preview ? (
              <img
                src={preview}
                alt="preview"
                className="rounded-xl w-full h-56 object-cover border border-slate-700"
                onError={(e) => { e.currentTarget.onerror = null; e.currentTarget.src = PLACEHOLDER; }}
              />
            ) : (
              <div className="rounded-xl border border-dashed border-slate-700 h-56 grid place-content-center text-slate-500">
                <Camera className="h-8 w-8 mx-auto mb-2" /> Preview
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-900/60 border border-slate-700/60">
          <CardContent className="grid grid-cols-2 gap-4 pt-6">
            <LabeledSelect label="Theme" value={theme} onChange={(e) => setTheme(e.target.value)}>
              {THEMES.map((t) => <option key={t} value={t}>{t}</option>)}
            </LabeledSelect>
            <LabeledSelect label="Product Type" value={ptype} onChange={(e) => setPtype(e.target.value)}>
              {Object.entries(PRODUCT_TYPES).map(([grp, items]) => (
                <optgroup key={grp} label={grp}>
                  {items.map((i) => <option key={i} value={i}>{i}</option>)}
                </optgroup>
              ))}
            </LabeledSelect>

            <LabeledSelect label="Style / Tone" value={tone} onChange={(e) => setTone(e.target.value)}>
              {TONES.map((t) => <option key={t} value={t}>{t}</option>)}
            </LabeledSelect>
            <LabeledSelect label="Language" value={lang} onChange={(e) => setLang(e.target.value)}>
              {LANGS.map(([code, name]) => <option key={code} value={code}>{name}</option>)}
            </LabeledSelect>
          </CardContent>
        </Card>
      </div>

      {/* RIGHT */}
      <div className="col-span-12 lg:col-span-8 space-y-6">
        <Card className="bg-slate-900/60 border border-slate-700/60">
          <CardHeader><CardTitle className="text-slate-100">Basics</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <FloatInput label="Product Name" value={name} onChange={(e) => setName(e.target.value)} />

            <div className="grid grid-cols-2 gap-4">
              <FloatInput label="Region (e.g., Karnataka, India)" value={region} onChange={(e) => setRegion(e.target.value)} />
              <FloatInput label="Artisan (name / id)" value={artisan} onChange={(e) => setArtisan(e.target.value)} />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <FloatInput label="Price" type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
              <LabeledSelect label="Currency" value={currency} onChange={(e) => setCurrency(e.target.value)}>
                {CURRENCIES.map((c) => <option key={c} value={c}>{c}</option>)}
              </LabeledSelect>
              <FloatInput label="Inventory" type="number" value={inventory} onChange={(e) => setInventory(e.target.value)} />
            </div>
          </CardContent>
        </Card>

        <KVEditor title="Attributes" rows={attrs} setRows={setAttrs} />
        <KVEditor title="Provenance" rows={prov} setRows={setProv} />

        <Card className="bg-slate-900/60 border border-slate-700/60">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-slate-100">
              <Wand2 className="h-5 w-5 text-sky-300" /> Storytelling
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <FloatTextarea label="Generate or write your own product description..." value={desc} onChange={(e) => setDesc(e.target.value)} />
            <Button onClick={genDescQuickHistory} disabled={busy} className={primaryBtn}>
              {busy ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Wand2 className="h-4 w-4 mr-2" />} Generate Story
            </Button>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-2 gap-4">
          <Card className="bg-slate-900/60 border border-slate-700/60">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-slate-100">
                <Sparkles className="h-5 w-5 text-sky-300" /> Social Post
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <FloatTextarea label="Generate catchy posts & taglines… (Markdown supported)" value={post} onChange={(e) => setPost(e.target.value)} />
              <Button onClick={genMarketing} disabled={busy} className={primaryBtn}>
                {busy ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Sparkles className="h-4 w-4 mr-2" />} Generate Marketing
              </Button>
              {(post || imageUrls.length > 0) && (
                <div className="space-y-2 rounded-xl border border-slate-700 p-3 bg-slate-800/60">
                  {imageUrls.length > 0 && (
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      {imageUrls.map((u) => (
                        <img key={u} src={u} alt="" className="w-full h-28 object-cover rounded-lg border border-slate-700" />
                      ))}
                    </div>
                  )}
                  <div className="prose prose-invert max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{post}</ReactMarkdown>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="bg-slate-900/60 border border-slate-700/60">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-slate-100">
                <Wand2 className="h-5 w-5 text-sky-300" /> AI Description
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <FloatTextarea label="Heritage, provenance, artisan journey…" value={story} onChange={(e) => setStory(e.target.value)} />
              <Button onClick={genStory} disabled={busy} className={primaryBtn}>
                {busy ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Wand2 className="h-4 w-4 mr-2" />} Generate Description
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );

  if (mode === "page")
  return (
    <div className="w-screen min-h-screen bg-slate-950 text-slate-100">
      <div className="sticky top-0 z-40 border-b border-slate-800 bg-slate-950/95 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button variant="ghost" onClick={onClose} className="text-slate-300 hover:text-sky-300">
              <ArrowLeft className="h-4 w-4 mr-1" /> Back
            </Button>
            <div className="font-semibold">Add New Item</div>
          </div>
          <div className="flex items-center gap-2">
            {err ? <div className="text-xs text-rose-400 pr-2">{err}</div> : null}
            <Button
              className={primaryBtn}
              disabled={busy}
              onClick={async () => {
                if (!name.trim()) return setErr("Please enter a product name.");
                if (!ptype) return setErr("Please select a product type.");
                try {
                  setErr("");
                  const id = slug(name || "Untitled");
                  const payload = buildProductPayload({ id });
                  if (payload.images) {
                    payload.images = payload.images.filter(
                      (u) => typeof u === "string" && !u.startsWith("/placeholder-")
                    );
                    if (payload.images.length === 0) delete payload.images;
                  }
                  console.log("POST /v1/products payload.images =", payload.images);
                  await jsonFetch(`/v1/products/${id}`, { method: "POST", body: JSON.stringify(payload) });
                  onCreate?.({
                    id,
                    name: name || "Untitled",
                    theme,
                    type: ptype,
                    preview: primaryImage,
                    inventory: Number.isFinite(+inventory) ? +inventory : 1,
                  });
                  onClose?.();
                } catch (e) {
                  setErr(String(e?.message || e || "Save failed"));
                }
              }}
            >
              <Plus className="h-4 w-4 mr-1" /> Save Item
            </Button>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-4 py-6">{Content}</div>
    </div>
  );

  // modal fallback (if ever used)
  return (
    <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
      <div className="absolute inset-0 -z-10 blur-3xl opacity-50 bg-gradient-to-b from-sky-900/30 via-transparent to-transparent" />
      <div className="w-full md:w-[1050px] rounded-2xl overflow-hidden shadow-2xl bg-slate-900/90 border border-slate-700/60 text-slate-100">
        <div className="p-4 border-b border-slate-700/60 bg-slate-900/60 flex items-center justify-between">
          <div className="flex items-center gap-2"><Plus className="h-5 w-5 text-sky-300" /><span className="font-semibold">Add New Item</span></div>
          <Button variant="ghost" onClick={onClose} className="text-slate-300 hover:text-sky-300">Close</Button>
        </div>
        <div className="p-6">{Content}</div>
      </div>
    </div>
  );
}
