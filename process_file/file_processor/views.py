import os
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import File
from django.core.exceptions import ObjectDoesNotExist

from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import io
import json

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
import PyPDF2
from docx import Document

# MongoDB configuration
client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000")
db = client["files"]
collection = db['files']

# Create your views here.
class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            data = json.loads(request.body)
            file_id = data.get("file_id")
            print(f"File Id recieved: {file_id}")

            if not file_id:
                return Response(data={"error": "ID not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                file_by_id = collection.find_one({"_id": ObjectId(file_id)})
                file_name = file_by_id["fileName"]
                print(f"File name is: {file_name}")
                
                # Save the file temporarily
                file_path = f"/tmp/{file_name}"
                # Write the content to the file
                with open(file_path, "w") as temp_file:
                    temp_file.write(file_by_id["data"])

                dataframe = self.read_doc_or_pdf(file_path)
                # accuracy = self.perform_ml_operation(dataframe)
                return Response(data={"Fild Id:": file_id}, status=status.HTTP_200_OK)
            
            except ObjectDoesNotExist:
                return Response(data={"error": f"No data found for ID: {file_id}"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print("Hello world")
                return Response(data={"error": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({"error": "Invalid request method"}, status=405)


    def read_doc_or_pdf(file_path: str):
        """
        Reads the content of a .docx or .pdf file and returns it as a PySpark DataFrame.

        Args:
            file_path (str): The file path to the .docx or .pdf file.

        Returns:
            pyspark.sql.DataFrame: A DataFrame with the file's content.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Initialize Spark session
        spark = SparkSession.builder.appName("ReadDocOrPdf").getOrCreate()

        file_extension = file_path.split('.')[-1].lower()

        content = ""
        if file_extension == "pdf":
            # Reading PDF file
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    content += page.extract_text() + "\n"
        elif file_extension == "docx":
            # Reading DOCX file
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
        else:
            raise ValueError("Unsupported file type. Please provide a .docx or .pdf file.")

        # Convert the content into a DataFrame
        data = [(line,) for line in content.split("\n") if line.strip()]
        schema = StructType([StructField("Content", StringType(), True)])
        df = spark.createDataFrame(data, schema)

        return df


    def perform_ml_operation(dataframe):
        pass
