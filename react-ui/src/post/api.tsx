import { Post } from './post';
import refreshAuth from '../auth';

export function getPost(id: number): Promise<Post>
{
    let access_token: string | null = sessionStorage.getItem("jwt_access_token");
    
    let promise = fetch(`${process.env.REACT_APP_FLASK_BASE_URL}/api/crud/post`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
    }
    ).then((response) => {
        return response.json();
    }).then((post_json) => {
        return {
            id: post_json.id,
            text: post_json.text,
            poster_id: post_json.poster.id,
            poster_username: post_json.poster.username,
            poster_email_hash: post_json.poster.email_hash,
            recipient_id: post_json.recipient_id,
            datetime: Date.parse(post_json.datetime)
        };
    });

    return promise;
}

export async function getPosts(): Promise<Array<Post>>
{
    let access_token: string | null = sessionStorage.getItem("jwt_access_token");
    
    let iter = 0;
    let sh_continue: boolean = true;
    let post_json: any;

    while (sh_continue)
    {
        let response = await fetch(`${process.env.REACT_APP_FLASK_BASE_URL}/api/crud/posts`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });
        
        if (response.status === 200)
        {
            post_json = await response.json();
            sh_continue = false;
        } else if (response.status === 401) 
        {
            if (iter != 0)
            {
                throw response;
            }

            let status_code = await refreshAuth();   
            
            if (status_code === 200)
            {
                iter += 1;
                continue
            } else
            {
                throw response;
            }
        } else {
            throw response;
        }
        iter += 1;
    }

    let api_posts: Array<any> = post_json;
    // console.log(api_posts);
    let posts: Array<Post>;
    posts = api_posts.map((value: any, index: number, array: any[]) : Post => {
        return {
            id: value.id,
            text: value.text,
            poster_id: value.poster.id,
            poster_username: value.poster.username,
            poster_email_hash: value.poster.email_hash,
            recipient_id: value,
            datetime: Date.parse(value.datetime)
        };
    });

    return posts;
}