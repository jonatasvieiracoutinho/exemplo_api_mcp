export type Book = {
  id: number
  title: string
  author?: string | null
  publisher?: string | null
  purchase_link?: string | null
  created_at: string
}

export type BookPayload = {
  title: string
  author?: string | null
  publisher?: string | null
  purchase_link?: string | null
}
