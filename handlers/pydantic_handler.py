from cleanapi.server import PydanticHandler
from pydantic import BaseModel, validator, NonNegativeInt
from typing import Optional, List


url_tail = '/pydantic.json'


class PydanticRequest(BaseModel):
    """
    Pydantic dataclass for request
    """
    foo: NonNegativeInt
    bar: NonNegativeInt

    @validator('foo', 'bar')
    def _validate_user_id(cls, val: str):
        if val == 666:
            raise ValueError(f'Values of foo and bar should not be equal to 666')
        return val


class PydanticResponse(BaseModel):
    """
    Pydantic dataclass for response
    """
    summ: Optional[NonNegativeInt]
    errors: Optional[List[dict]]


# noinspection PyAbstractClass
class Handler(PydanticHandler):
    """
    Example of using PydanticHandler
    """
    request_dataclass = PydanticRequest
    result_dataclass = PydanticResponse

    # noinspection PyUnusedLocal
    def process(self, request: request_dataclass) -> result_dataclass:
        """
        What the handler should do
        :param request: incoming request
        :type request: request_dataclass
        :return: processing result
        :type: result_data class
        """
        result = PydanticResponse(summ=request.foo + request.bar, errors=[])

        if result.summ > 500:
            raise ValueError('The sum of foo and bar is more than 1000')

        return result

    def if_exception(self, errors: list) -> None:
        """
        What to do if an exception was thrown
        :param errors: list of errors
        :type errors: list
        """
        self.set_status(400)
        self.write({'errors': errors})
        return
