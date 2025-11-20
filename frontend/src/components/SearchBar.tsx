type Props = {
  value: string
  onChange: (value: string) => void
  onSearch: () => void
}

// Input simples + botao usados para disparar a busca.
export function SearchBar({ value, onChange, onSearch }: Props) {
  return (
    <div className="search-bar">
      <input
        placeholder="Buscar por titulo, autor ou editora"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
      <button onClick={onSearch}>Buscar</button>
    </div>
  )
}
