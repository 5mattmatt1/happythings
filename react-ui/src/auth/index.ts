// Might want to make a wrapper around fetch like authFetch or something...

export default async function refreshAuth(): Promise<number>
{
    let refresh_token: string | null = sessionStorage.getItem("jwt_refresh_token");

    let response = await fetch(`${process.env.REACT_APP_FLASK_BASE_URL}/api/auth/refresh`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${refresh_token}`
        },
    });

    if (response.status != 200)
    {
        throw response;
    }

    let auth_json = await response.json();
    sessionStorage.setItem("jwt_access_token", auth_json.refresh.access_token);

    return response.status;
}