from langchain.tools import Tool
import ocr_tool, rag_tool, api_tool

OCR_TOOL = Tool(
    name="Extract_info_from_files",
    func=ocr_tool.convert_file,
    description="Extract all the data from the given image/pdf/docx file path and save it to text file"
)

API_TOOL = Tool(
    name="collect_weather_data",
    func=api_tool.get_weather,
    description="Extract weather information of the given city "
)

RAG_TOOL = Tool(
    name="retrieve_document",
    func=rag_tool.get_retriever,
    description="search documents for medical related information"
)
