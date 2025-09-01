import { useState } from "react";

const PLACEHOLDER = "/placeholder-640x360.png";

export default function SafeImage({ src, alt = "", className = "" }) {
  const [failed, setFailed] = useState(false);
  const url = !src || failed ? PLACEHOLDER : src;
  return (
    <img
      src={url}
      alt={alt}
      onError={() => setFailed(true)}
      className={className}
      loading="lazy"
    />
  );
}
