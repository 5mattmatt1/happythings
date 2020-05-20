export interface Post
{
    id: number,
    text: string,
    poster_id: number,
    poster_username: string,
    poster_email_hash: string,
    recipient_id: number,
    datetime: number
}