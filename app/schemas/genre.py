from pydantic import BaseModel


class Page(int):
    pass


class Size(int):
    pass


class GenreId(int):
    pass


class GenreName(str):
    pass


class GenreCreateOrUpdate(BaseModel):
    name: GenreName


class GenreCreateRequestV1(GenreCreateOrUpdate):
    pass


class GenreDetails(BaseModel):
    id: GenreId
    name: GenreName


class GenreBase(BaseModel):
    id: GenreId
    name: GenreName


class GenreGetListResponseV1(BaseModel):
    genres: list[GenreBase]
    page: Page
    size: Size


class GenreCreateResponseV1(GenreDetails):
    pass


class GenreGetDetailsResponseV1(GenreDetails):
    pass


class GenreAlreadyExistsException(Exception):
    pass


class GenreNotFoundException(Exception):
    pass
