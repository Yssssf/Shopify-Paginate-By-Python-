import requests

# Request Json parameters from GraphQL
def fetch_shopify_data(api_url, headers, query, variables=None):
    response = requests.post(api_url, json={'query': query, 'variables': variables}, headers=headers)
    response_data = response.json()
    # Handling errors
    if 'errors' in response_data:
        raise Exception(f"Error fetching data: {response_data['errors']}")
    
    return response_data

# Paginate the data

def fetch_paginated_data(api_url, headers, query, page_size=100):
    all_items = []
    has_next_page = True
    end_cursor = None

    while has_next_page:
        variables = {
            'first': page_size,
            'after': end_cursor
        }

        # Execute the request
        response_data = fetch_shopify_data(api_url, headers, query, variables)
        items = response_data['data']['products']['edges']
        all_items.extend(items)
        
        # Pagination info
        page_info = response_data['data']['products']['pageInfo']
        has_next_page = page_info['hasNextPage']
        end_cursor = page_info['endCursor']
        
        print(f"Fetched {len(items)} items, Total so far: {len(all_items)}")

    return all_items

# Shopify API endpoint and headers
# ACCESS_TOKEN (replace with your actual API access token)
API_URL = "https://quickstart-886385b5.myshopify.com/admin/api/2024-10/graphql.json"
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# GraphQL query to fetch products with pagination
GRAPHQL_QUERY = """
query ($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    edges {
      node {
        id
        title
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

# Fetch all paginated data
all_products = fetch_paginated_data(API_URL, HEADERS, GRAPHQL_QUERY)
print(f"Total products fetched: {len(all_products)}")