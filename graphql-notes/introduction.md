## What's the difference between GraphQL and a REST API?
- We only define a single endpoint (for example http://example/graphql).
- Since this is a query language, all actions are done through a POST .

It means we query directly the only endpoint requesting for specific data.

### Types of operations
Every GraphQL schema has three special root types: Query, Mutation, and Subscription. The root types correspond to the three operation types offered by GraphQL: queries, mutations, and subscriptions. The fields on these root types are called root fields and define the available API operations.
- Query: We will look for specific data (equivalent to a GET, but selecting the attributes of our choice)
- Mutation: We want to change the data (we can compare it to the POST, PUT, and DELETE actions)
- Subscription: A bit special case that allows you to maintain a connection with the remote server by making use of WebSockets

### Queries
`resolve` is the name of the resolver function of the feed query. A resolver is the implementation for a GraphQL field. Every field on each type (including the root types) has a resolver function which is executed to get the return value when fetching that type. For now, our resolver implementation is very simple, it just returns the links array. The resolve function has four arguments, parent, args, context and info. 

So, for example, if you have a type as follows 
```js
export const Link = objectType({
	name: 'Link', // name of the type
	definition(t) {
		// all fields of the type
		t.nonNull.int('id');
		t.nonNull.string('description');
		t.nonNull.string('url');
	},
});
```

Link is the root type, and id, description and url are its fields.
In this example, we would need a resolve function for each of the fields.

### Batched resolving - how GraphQL works under the hood
https://www.howtographql.com/advanced/1-server/

Every field in the query can be associated with a type:
```js
query: Query {
  author(id: "abc"): Author {
    posts: [Post] {
      title: String
      content: String
    }
  }
}
```

As every field has a resolver, what GraphQL does is basically invoke each one and kind of curry its results.
A resolver is like a "controller" - it contains the logic to fetch the stuff, but sometimes graphQL can infer how this process happens; i.e if we are fetching objects of type list, they will be fetched one by one



Now, we can easily find the resolvers in our server to run for every field. The execution starts at the query type and goes breadth-first. This means we run the resolver for Query.author first. Then, we take the result of that resolver, and pass it into its child, the resolver for Author.posts. At the next level, the result is a list, so in that case, the execution algorithm runs on one item at a time. So the execution works like this:

```
//ps: note the four parameters passed to each resolver

Query.author(root, { id: 'abc' }, context) -> author
Author.posts(author, null, context) -> posts
for each post in posts
  Post.title(post, null, context) -> title
  Post.content(post, null, context) -> content
```

But sometimes you might end up making "redundant" requests, like fetching multiple times an author of a post (since they
can write multiple posts)

So, to avoid this
```js
fetch('/authors/1')
fetch('/authors/2')
fetch('/authors/1')
fetch('/authors/2')
fetch('/authors/1')
fetch('/authors/2')
```

We write the **loaders**:
```js
authorLoader = new AuthorLoader()

// Queue up a bunch of fetches
authorLoader.load(1);
authorLoader.load(2);
authorLoader.load(1);
authorLoader.load(2);

// Then, the loader only does the minimal amount of work
fetch('/authors/1');
fetch('/authors/2');

```

## Fetching information from our GraphQL backend (making queries)
First, we need to understand how we must write the queries.
Let's start with a practical example then:
### 1 - Defining things in our graphQL server: Root Types
**GraphQL queries begin from root types: query, mutation, and subscription.** It means that, on top-level, we need to define the format (types) of these root types; not all of them, but at least the query type, otherwise we'll get an error on the server.
```js
import { GraphQLSchema } from 'graphql';
import { MutationType } from './mutationType';
import { QueryType } from './queryType';

export const schema = new GraphQLSchema({
  query: QueryType,
  mutation: MutationType,
});

```
Okay, now we have the structure of both queries and mutations. Now, let's see how they are:
### 1 - `GraphQLObjectType`: the format of our objects
```js
import { GraphQLObjectType, GraphQLString, GraphQLNonNull } from 'graphql';
import { User } from './userModel';

export const UserType = new GraphQLObjectType<User>({
  name: 'User',
  fields: () => ({
    username: {
      type: new GraphQLNonNull(GraphQLString),
      resolve: (user) => user.username,
    },
    displayName: {
      type: GraphQLString,
      resolve: (user) => user.displayName,
    },
    birthday: {
      type: new GraphQLNonNull(GraphQLString),
      resolve: (user) => user.birthday,
    },
    email: {
      type: new GraphQLNonNull(GraphQLString),
      resolve: (user) => user.email,
    },
    password: {
      type: new GraphQLNonNull(GraphQLString),
      resolve: (user) => user.password,
    },
  }),
});
```

To query a information, we need firstly to define the **format** of this info, and here it is achieved by creating a `GraphQLObjectType`. This defined type is going to be used when we define the format of our **query**.
```js
import {
  GraphQLList,
  GraphQLObjectType,
} from 'graphql';
import { UserModel } from '../modules/user/userModel';
import { UserType } from '../modules/user/userType';

export const QueryType = new GraphQLObjectType({
  name: 'Query',
  description: 'Find all users',
  fields: {
    allUsers: {
      type: new GraphQLList(UserType), // this query returns a list of our previously defined type
      async resolve(parent, args) {
        const user = await UserModel.find({});
        return user;
      },
    },
  },
});

```

An important thing to notice here: the use of a **resolve** function. 
The resolver functions, in GraphQL, play a role in fetching the information from our database - or from somewhere else.
They are like the controllers in the MVC model, and here we use them to define a `find` that simply fetches all the users contained in our database (we are using MongoDB here).

### But how do we make a request to our graphQL server to get all users?
First, let's remember that all requests to a GraphQL API are made through POSTs. So, we can make this work using `fetch` in Node: 
```js
import fetch from 'node-fetch';
async function fetchGraphQL(textQuery: string) {
	const response = await fetch('http://localhost:3005/graphql', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			query: textQuery,
		}),
	});

	const res = await response.json();
	console.log(res.data);
}

fetchGraphQL(`
{
 allUsers {
    username,
    email
  }
}
`);
```

It replicates what we'd be doing in GraphiQL, for example:
![graphiql](https://user-images.githubusercontent.com/57643375/179418142-b08e406b-983f-452b-aa20-c8ceee55cd68.png)

We are sending a JSON with all the fields we want to receive back. As a response, we get each the `username` and `email` fields from all our users. 
