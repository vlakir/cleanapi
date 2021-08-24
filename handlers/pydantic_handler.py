from cleanapi.server import PydanticHandler
from pydantic import BaseModel, validator, NonNegativeInt
import json
from typing import Optional, List


url_tail = '/pydantic.json'


# noinspection PyAbstractClass
class Handler(PydanticHandler):
    """
    Example of using PydanticHandler
    """
    async def post(self):
        try:
            body_json_dict = json.loads(self.request.body)
            request = PydanticRequest(**body_json_dict)
        except (json.decoder.JSONDecodeError, TypeError, ValueError) as ex:
            print(str(ex))
            self.set_status(400)
            self.write({'critical_error': str(ex)})
            return

        result = PydanticResponse(summ=request.foo + request.bar)

        if result.summ > 500:
            result.summ = None
            result.errors = []
            result.errors.append({'error': 'The sum of foo and bar is more than 1000'})

        output_json = result.json(exclude_none=True)

        self.set_status(200)
        self.write(output_json)


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
