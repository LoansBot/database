# Endpoint Params

Describes the parameters to a particular endpoint.

Fields:
- `id (serial, primary key)`: The surrogate identifier for this row
- `endpoint_id (integer, references endpoints(id) on delete cascade)`:
  The endpoint this is a parameter for.
- `location (text)`: Describes where this parameter lives. Acts as an enum
  and takes one of the following values:
  - `query`: Query parameter.
  - `body`: Body parameters.
  - `header`: Header parameters.
- `path (text)`: Acts as a list of strings separated by dots which is how to get
  to the parameter within the location. For query and header parameters this is
  always blank. For body parameters it can have an arbitrary length, e.g., for
  the body `{"foo": { "bar": 7 }}` it has one body parameter with a blank path
  and name `foo` and one parameter with the path `foo` and name `bar`. All
  partial paths must be specified since this may use that for discovery.
- `name (text)`: The name of the variable at this location and path.
- `var_type (text)`: The type of variable. The format is not enforced, but
  should in general follow the same style we use in the web-backend python
  code (e.g., `str, None`, `dict`, or `list[int]`)
- `description_markdown (text)`: The markdown description of this parameter.
  Should be standadr markdown and ideally only the subset that reddit supports.
- `added_date (date)`: When this parameter was added to the endpoint. We do not
  support parameter removal from an endpoint without going through a full
  endpoint sunsetting currently.

## Schema

```
                                                       Table "public.endpoint_params"
        Column        |  Type   | Collation | Nullable |                   Default                   | Storage  | Stats target | Description
----------------------+---------+-----------+----------+---------------------------------------------+----------+--------------+-------------
 id                   | integer |           | not null | nextval('endpoint_params_id_seq'::regclass) | plain    |              |
 endpoint_id          | integer |           | not null |                                             | plain    |              |
 location             | text    |           | not null |                                             | extended |              |
 path                 | text    |           | not null |                                             | extended |              |
 name                 | text    |           | not null |                                             | extended |              |
 var_type             | text    |           | not null |                                             | extended |              |
 description_markdown | text    |           | not null |                                             | extended |              |
 added_date           | date    |           | not null | CURRENT_DATE                                | plain    |              |
Indexes:
    "endpoint_params_pkey" PRIMARY KEY, btree (id)
    "index_endpoint_params_on_ep_loc_path_name" UNIQUE, btree (endpoint_id, location, path, name)
Foreign-key constraints:
    "endpoint_params_endpoint_id_fkey" FOREIGN KEY (endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
```
