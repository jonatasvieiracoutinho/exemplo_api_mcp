import apiClient from './client'
import type { Book, BookPayload } from '../types/book'

// Wrappers tipados para os endpoints FastAPI /api/books.
export async function listBooks(params?: { limit?: number; offset?: number }): Promise<Book[]> {
  const response = await apiClient.get<Book[]>('/books', { params })
  return response.data
}

export async function searchBooks(query: string, params?: { limit?: number; offset?: number }): Promise<Book[]> {
  const response = await apiClient.get<Book[]>('/books/search', { params: { query, ...params } })
  return response.data
}

export async function createBook(payload: BookPayload): Promise<Book> {
  const response = await apiClient.post<Book>('/books', payload)
  return response.data
}

export async function updateBook(id: number, payload: BookPayload): Promise<Book> {
  const response = await apiClient.put<Book>(`/books/${id}`, payload)
  return response.data
}

export async function patchBook(id: number, payload: Partial<BookPayload>): Promise<Book> {
  const response = await apiClient.patch<Book>(`/books/${id}`, payload)
  return response.data
}

export async function deleteBook(id: number): Promise<void> {
  await apiClient.delete(`/books/${id}`)
}
