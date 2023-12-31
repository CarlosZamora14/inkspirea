from urllib.parse import urlparse, urlsplit, urlunsplit, quote, unquote, parse_qs


def extract_base_url(url: str) -> str:
  parsed_url = urlsplit(url)
  base_url = urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', ''))
  return base_url


def extract_query_string_parameter(url: str, parameter: str) -> str | None:
  parsed_url = urlparse(url)
  query_params = parse_qs(parsed_url.query)
  value = query_params.get(parameter, [None])[0]
  return value


def encode_next_url(url: str | None) -> str | None:
  if url is not None:
    return quote(url, safe='')

  return url


def decode_next_url(url: str | None) -> str | None:
  if url is not None and '%' in url:
    return unquote(url)

  return url