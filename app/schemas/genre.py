from pydantic import BaseModel


class GenreName(str):
    pass


class GenreId(int):
    pass


class GenreCreateOrUpdate(BaseModel):
    name: GenreName


class GenreCreateRequestV1(GenreCreateOrUpdate):
    pass


class GenreDetails(BaseModel):
    id: GenreId
    name: GenreName


class GenreCreateResponseV1(GenreDetails):
    pass


class GenreAlreadyExistsException(Exception):
    pass
