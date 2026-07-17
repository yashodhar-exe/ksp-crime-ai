interface IconProps {
  name: string;
  className?: string;
  filled?: boolean;
}

/** Wraps Google's Material Symbols Outlined font, loaded in index.html. */
export function Icon({ name, className = "", filled = false }: IconProps) {
  return (
    <span
      className={`material-symbols-outlined select-none ${className}`}
      style={{ fontVariationSettings: filled ? "'FILL' 1" : "'FILL' 0" }}
    >
      {name}
    </span>
  );
}
