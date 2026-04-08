from paddleocr import PaddleOCRVL

pipeline = PaddleOCRVL(pipeline_version="v1.5")
output = pipeline.predict("iso/iso20_spec.pdf")

for res in output:
    res.save_to_json(save_path="OCR_output_1.5/json")
    res.save_to_markdown(save_path="OCR_output_1.5/markdown")
