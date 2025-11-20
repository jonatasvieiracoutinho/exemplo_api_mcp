import { useEffect, useState } from 'react'
import type { Book, BookPayload } from '../types/book'
import { BookForm } from '../components/BookForm'
import { BookTable } from '../components/BookTable'
import { SearchBar } from '../components/SearchBar'
import { createBook, deleteBook, listBooks, searchBooks, updateBook } from '../api/books'

// Pagina principal: coordena buscas, CRUD e renderizacao dos componentes.
// A API nao exige autenticacao porque o objetivo e somente demonstrar o fluxo.
export function BooksPage() {
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [activeBook, setActiveBook] = useState<Book | null>(null)

  const fetchBooks = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = searchTerm ? await searchBooks(searchTerm) : await listBooks()
      setBooks(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar livros')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchBooks()
  }, [])

  const handleSubmit = async (payload: BookPayload, editingId?: number) => {
    if (editingId) {
      await updateBook(editingId, payload)
    } else {
      await createBook(payload)
    }
    setActiveBook(null)
    await fetchBooks()
  }

  const handleDelete = async (book: Book) => {
    if (!confirm(`Deseja excluir o livro "${book.title}"?`)) {
      return
    }
    await deleteBook(book.id)
    await fetchBooks()
  }

  const handleSearch = async () => {
    await fetchBooks()
  }

  return (
    <div className="container">
      <header>
        <div>
          <h1>Catálogo de Livros</h1>
          <p>Gerencie sua lista de livros em um só lugar.</p>
        </div>
      </header>

      <SearchBar value={searchTerm} onChange={setSearchTerm} onSearch={handleSearch} />

      <div className="grid">
        <BookForm onSubmit={handleSubmit} activeBook={activeBook} onCancel={() => setActiveBook(null)} />
        <section className="card">
          <h2>Lista</h2>
          {error && <p className="error">{error}</p>}
          {loading ? <p>Carregando...</p> : <BookTable books={books} onEdit={setActiveBook} onDelete={handleDelete} />}
        </section>
      </div>
    </div>
  )
}
