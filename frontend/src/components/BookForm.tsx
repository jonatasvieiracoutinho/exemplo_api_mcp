import { useEffect, useState } from 'react'
import type { Book, BookPayload } from '../types/book'

type Props = {
  onSubmit: (payload: BookPayload, editingId?: number) => Promise<void>
  activeBook?: Book | null
  onCancel: () => void
}

const emptyPayload: BookPayload = {
  title: '',
  author: '',
  publisher: '',
  purchase_link: '',
}

// Formulario controlado usado tanto para criar quanto para editar livros.
export function BookForm({ onSubmit, activeBook, onCancel }: Props) {
  const [form, setForm] = useState<BookPayload>(emptyPayload)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (activeBook) {
      setForm({
        title: activeBook.title,
        author: activeBook.author ?? '',
        publisher: activeBook.publisher ?? '',
        purchase_link: activeBook.purchase_link ?? '',
      })
    } else {
      setForm(emptyPayload)
    }
  }, [activeBook])

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await onSubmit(
        {
          title: form.title.trim(),
          author: form.author?.trim() || undefined,
          publisher: form.publisher?.trim() || undefined,
          purchase_link: form.purchase_link?.trim() || undefined,
        },
        activeBook?.id,
      )
      setForm(emptyPayload)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao salvar livro')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2>{activeBook ? 'Editar livro' : 'Adicionar livro'}</h2>
      <label>
        Título*
        <input name="title" value={form.title} onChange={handleChange} required />
      </label>
      <label>
        Autor
        <input name="author" value={form.author || ''} onChange={handleChange} />
      </label>
      <label>
        Editora
        <input name="publisher" value={form.publisher || ''} onChange={handleChange} />
      </label>
      <label>
        Link de compra
        <input name="purchase_link" value={form.purchase_link || ''} onChange={handleChange} />
      </label>
      {error && <p className="error">{error}</p>}
      <div className="form-actions">
        <button type="submit" disabled={loading}>
          {loading ? 'Salvando...' : activeBook ? 'Salvar alterações' : 'Adicionar'}
        </button>
        {activeBook && (
          <button type="button" className="secondary" onClick={onCancel} disabled={loading}>
            Cancelar
          </button>
        )}
      </div>
    </form>
  )
}
