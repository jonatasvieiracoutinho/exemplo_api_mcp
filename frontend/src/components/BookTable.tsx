import type { Book } from '../types/book'

type Props = {
  books: Book[]
  onEdit: (book: Book) => void
  onDelete: (book: Book) => void
}

// Tabela de apresentacao: apenas mostra dados e dispara callbacks.
export function BookTable({ books, onEdit, onDelete }: Props) {
  if (!books.length) {
    return <p>Nenhum livro encontrado.</p>
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Autor</th>
            <th>Editora</th>
            <th>Link</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {books.map((book) => (
            <tr key={book.id}>
              <td>{book.title}</td>
              <td>{book.author || '-'}</td>
              <td>{book.publisher || '-'}</td>
              <td>
                {book.purchase_link ? (
                  <a href={book.purchase_link} target="_blank" rel="noreferrer">
                    Comprar
                  </a>
                ) : (
                  '-'
                )}
              </td>
              <td>
                <button onClick={() => onEdit(book)}>Editar</button>
                <button onClick={() => onDelete(book)} className="danger">
                  Excluir
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
