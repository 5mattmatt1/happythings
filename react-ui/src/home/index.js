import React, { useState, useEffect } from 'react';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Pagination from '@material-ui/lab/Pagination';

import { PostComponent, getPosts } from '../post';
import io from 'socket.io-client';

export default function Home() 
{  
  // Probably want to move some of this up to a PostsComponent that
  // encapsulate PostComponent
  const [posts, setPosts] = React.useState([]);
  // const [rows, setRows] = React.useState([]);
  const socket = io(`${process.env.REACT_APP_FLASK_BASE_URL}`);
  
  function updatePosts()
  {
    console.log(getPosts);
    getPosts().then((posts) => {
      // console.log(posts);
      posts.sort((a, b) => {
        return -(a.datetime - b.datetime);
      });

      setPosts(posts);
    }).catch((error) => {
      console.error(error);
      error.json().then((json) => {
        console.log(json);
      });

      // Status Code: 422
      window.location.href = "/login";
    });
  }
  
  socket.on("new_post", () => {
    updatePosts();
  });

  useEffect(() => {
    // Sort by latest datetime since they're the most relevant
    updatePosts();
  }, []);

  console.log(posts);
  let rows = [];
  for (let idx in posts)
  {
    let post = posts[idx];
    console.log(post);
    rows.push((
      <Grid item>
        <PostComponent post={post} key={post.id}>
        </PostComponent>
      </Grid>
    ));
  }

  return (
    <Container component="main" maxWidth="xs">
      <Grid container direction="column" spacing={3}>
        {rows}
      </Grid>
      {
        // Will probably be added in later.
        // <Pagination defaultPage={1} count={1} variant="outlined" />
      }
    </Container>
  );
}
