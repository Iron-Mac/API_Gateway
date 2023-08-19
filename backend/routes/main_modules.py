# from fastapi import APIRouter
# from schemas import Input1, Input2
# from utils.model_evaluation import print_word_tag
# from utils.TextRankMedium import textrank
# from utils.Roge import roge

# router = APIRouter()


# @router.post("/postager/")
# async def read_root(user_input: Input1):
#     res = print_word_tag(user_input.input_data)
#     return {"res": res}


# @router.post("/textrank/")
# async def read_root(user_input: Input1):
#     res = textrank(user_input.input_data)
#     return {"res": res}


# @router.post("/roge/")
# async def read_root(user_input: Input2):
#     res = roge(user_input.phrase1, user_input.phrase2)
#     return {"res": res}
