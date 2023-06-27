import os
import openai

openai.api_key = "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"

openai.File.create(
  file=open("newData.jsonl", "rb"),
  purpose='fine-tune'
)

print(openai.FineTune.list())
