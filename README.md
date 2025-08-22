# Dự án Phân Tích Bộ Dữ Liệu Tiểu Đường (Pima Indians Diabetes)

## Giới thiệu
Ứng dụng web tương tác được xây dựng bằng **Streamlit** để khám phá và làm sạch bộ dữ liệu **Pima Indians Diabetes**.  
Dự án tập trung vào **chuẩn bị dữ liệu, trực quan hóa và phân tích** thông qua các biểu đồ và bộ lọc tương tác.  
Ứng dụng cho phép người dùng **xem, làm sạch và xuất dữ liệu** mà không áp dụng các kỹ thuật học máy.

## Cấu trúc dự án
Diabetes_Dataset/

│── app.py # File chính chạy ứng dụng Streamlit

│── data_loader.py # Xử lý tải dữ liệu

│── data_cleaner.py # Làm sạch dữ liệu (xử lý giá trị 0, NaN)

│── plot.py # Vẽ biểu đồ bằng Plotly

│── data/diabetes.csv # Bộ dữ liệu đầu vào

│── README.md # Document


## Cách cài đặt và chạy dự án
1. **Clone dự án về máy**
   ```bash
   git clone https://github.com/your-username/diabetes-dataset.git
   cd diabetes-dataset
2. **Tạo môi trường ảo và cài đặt thư viện**
    ```bash
    python -m venv venv
    venv\Scripts\activate    # Trên Windows
    source venv/bin/activate # Trên macOS/Linux
    pip install -r requirements.txt
3. **Chạy ứng dụng Streamlit**
    ```bash
    streamlit run app.py
