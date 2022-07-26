# TYPES IN GRAPHQL

Vc nao pode por um `GraphQLObjectType` dentro de outro `GraphQLObjectType`

No top level, a gente tem o `GraphQLSchema`, que vai ter a definição geral dos schemas possíveis dentro de um server GraphQL.

Definição do `GraphQLSchema`:

```jsx
class GraphQLSchema {
  constructor(config: GraphQLSchemaConfig)
}

type GraphQLSchemaConfig = {
  query: GraphQLObjectType;
  mutation?: ?GraphQLObjectType;
}
```

**Ou seja, vc tem que definir ao menos uma `query`.**

Tanto query quanto mutations são GraphQLObjectTypes, 

### Definição de `GraphQLObjectType`

> An object type within GraphQL that contains fields.
> 

Esse tipo é usado, como vimos acima, para definir 

```jsx
class GraphQLObjectType {
  constructor(config: GraphQLObjectTypeConfig)
}
type GraphQLObjectTypeConfig = {
  name: string;
  interfaces?: GraphQLInterfacesThunk | Array<GraphQLInterfaceType>;
  fields: GraphQLFieldConfigMapThunk | GraphQLFieldConfigMap;
  isTypeOf?: (value: any, info?: GraphQLResolveInfo) => boolean;
  description?: ?string
}

```

Portanto, GraphQLObjectType pega um objeto contendo as configs.

**EXEMPLO DE CÓDIGO**

```jsx
import { GraphQLSchema } from 'graphql';
import { MutationType } from './mutationType';
import { QueryType } from './queryType';

export const schema = new GraphQLSchema({
  query: QueryType,
  mutation: MutationType,
});
```

Veja que na nossa definição do schema da aplicação (que é do tipo `GraphQLSchema`), temos uma query e uma mutation (ambas do tipo `GraphQLObjectType`)

Vamos agora ver a definição de cada um:

```jsx
import { GraphQLNonNull, GraphQLObjectType, GraphQLString } from 'graphql';
import * as userMutations from '../modules/user/mutations';

export const MutationType = new GraphQLObjectType({
  name: 'Mutation',
  description: 'Root of mutations',
	// fields: ThunkObjMap<GraphQLFieldConfig<unknown, unknown, any>>
  fields: () => ({
    ...userMutations,
  }),
});
```

Esse é o mutationType. O que vem dentro do `GraphQLObjectType` é do tipo `GraphQLObjectTypeConfig` (definição acima).

Agora, vamos entender o que vem dentro do campo fields: `GraphQLFieldConfigMapThunk | GraphQLFieldConfigMap`.

**Definição de** `GraphQLFieldConfigMap`:

```jsx
type GraphQLFieldConfigMap = {
  [fieldName: string]: GraphQLFieldConfig;
};

```

`GraphQLFieldConfig`:

```jsx
type GraphQLFieldConfig = {
  type: GraphQLOutputType;
  args?: GraphQLFieldConfigArgumentMap;
  resolve?: GraphQLFieldResolveFn;
  deprecationReason?: string;
  description?: ?string;
}

```

`GraphQLFieldConfigMapThunk`:

```jsx
type GraphQLFieldConfigMapThunk = () => GraphQLFieldConfigMap;
```

Obs: no exemplo abaixo, tanto quanto no exemplo com uma mutation, o tipo de fields é `fields: ThunkObjMap<GraphQLFieldConfig<any, any, any>>`

```tsx
export const QueryType = new GraphQLObjectType({
  name: 'Query',
  description: 'Root of queries',
  fields: () => ({
    VersionQuery
  }),
});
```

(aparentemente thunk é tipo uma função que retorna o tipo; no caso retornamos um objeto com um `GraphQLFieldConfig`, portanto nosso type é um ThunkObjMap com o tipo do objeto.

### Por que na mutation usamos o spread operator e na query não?

Na query, temos `VersionQuery: GraphQLFieldConfig<any, any, any>`

(definição de VersionQuery):

```tsx
import { GraphQLString, GraphQLNonNull, GraphQLFieldConfig } from 'graphql';

import { version as packageVersion } from '../../../../package.json';

export const VersionQuery: GraphQLFieldConfig<any, any, any> = {
  type: new GraphQLNonNull(GraphQLString),
  resolve: () => packageVersion,
};
```

Na mutation, é um pouco diferente, porque nós usamos uma definição do graphql-relay. Portanto temos que entender o tipo dessa definição.

```tsx
import { GraphQLNonNull, GraphQLString } from 'graphql';
import { mutationWithClientMutationId } from 'graphql-relay';
import { UserModel } from '../userModel';
import { UserType } from '../userType';

export const CreateUserMutation = mutationWithClientMutationId({
  name: 'CreateUser',
  description: 'Creates a new user',
  inputFields: {
    username: { type: new GraphQLNonNull(GraphQLString) },
    displayName: { type: new GraphQLNonNull(GraphQLString) },
    birthday: { type: new GraphQLNonNull(GraphQLString) },
    email: { type: new GraphQLNonNull(GraphQLString) },
    password: { type: new GraphQLNonNull(GraphQLString) },
  },

  mutateAndGetPayload: async ({ email, ...rest }) => {
    const user = new UserModel({
      ...rest,
      email,
    });

    return user.save();
  },

  outputFields: {
    user: {
      type: UserType,
      resolve: async ({ email }) => UserModel.findOne({ email }),
    },
  },
});
```

**Veja que o objeto** `CreateUserMutation` recebe as propriedades do tipo MutationConfig e é um objeto do tipo GraphQLFieldConfig.

```jsx
export declare function mutationWithClientMutationId(
  config: MutationConfig,
): GraphQLFieldConfig<unknown, unknown>;
export {};

interface MutationConfig {
  name: string;
  description?: string;
  deprecationReason?: string;
  extensions?: GraphQLFieldExtensions<any, any>;
  inputFields: ThunkObjMap<GraphQLInputFieldConfig>;
  outputFields: ThunkObjMap<GraphQLFieldConfig<any, any>>;
  mutateAndGetPayload: MutationFn;
}
```

Portanto, no mutation type,

```tsx
import { GraphQLNonNull, GraphQLObjectType, GraphQLString } from 'graphql';
import * as userMutations from '../modules/user/mutations';

export const MutationType = new GraphQLObjectType({
  name: 'Mutation',
  description: 'Root of mutations',
  fields: () => ({
    ...userMutations,
  }),
});
```

usamos o spread operator porque o tipo de userMutations é um GraphQLFieldConfig, e ao colocar esse objeto como o retorno de um field, temos um `fields: ThunkObjMap<GraphQLFieldConfig<unknown, unknown, any>>`, no mesmo formato do da query.