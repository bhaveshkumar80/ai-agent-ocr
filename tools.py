from langchain.tools import Tool
import ocr_tool, rag_tool, weather_tool

OCR_TOOL = Tool(
    name="Extract_info_from_files",
    func=ocr_tool.convert_file,
    description="Use this tool to extract text content from image, PDF, or DOCX files provided via a file path, converting them into plain text format for further analysis."
)

WEATHER_TOOL = Tool(
    name="collect_weather_data",
    func=weather_tool.get_weather,
    description="Use this tool to retrieve current and forecasted weather details (e.g., temperature, humidity, precipitation, wind) for a given location by fetching data from weather.com. Ideal for answering user questions about weather conditions."
)

RAG_TOOL = Tool(
    name="retrieve_document",
    func=rag_tool.get_retriever,
    description="Use this tool to search and retrieve relevant information from a medical document database in response to health or medicine-related queries."
)

NO_TOOL = Tool(
    name="NoToolNeeded",
    func=lambda _: "No tool needed — answer directly.",
    description="Select this if the question can be answered directly without any tool."
)