# SteamRecommendSystem: Using Collaborative Filtering

Đây là một dự án mà nhóm chúng tôi tạo ra để tìm hiểu kiến thức cơ bản của Machine Learning.

Một số thư viện mà chúng tôi sử dụng trong project: `numpy, pandas, sklearn, tkinter, random, csv`. 
Dự án sử dụng thuật toán `Collaborative Filtering` để đưa ra gợi ý cho người dùng các game mà người dùng có thể thích (quan tâm) dựa trên tập dữ liệu lấy từ [Steam Video Games | Kaggle](https://www.kaggle.com/datasets/tamber/steam-video-games?fbclid=IwAR3MSJ8ZaHPzQ5oUSXrGMXCNhTay5MDUO7srL9d7efFFw0YGWljnU5vNYDk).   

## Data Processing
  
 - *Tập dữ liệu:* [Steam Video Games | Kaggle](https://www.kaggle.com/datasets/tamber/steam-video-games?fbclid=IwAR3MSJ8ZaHPzQ5oUSXrGMXCNhTay5MDUO7srL9d7efFFw0YGWljnU5vNYDk).
 - *Đầu vào:* Dữ liệu gồm các phần tử `[UserId, Name, Hours]`
 - *Tiền xử lí dữ liệu* : Xử lí và lọc những phần tử lỗi (thiếu), đánh giá của từng user với mỗi item. Tập dữ liệu mới gồm các phần tử `[UserId, Name, Rating]`.

## Collaborative Filtering


### 1. User-User

  Dựa vào mức độ quan tâm của user tới item và sự tương đồng với user khác để đưa ra gợi ý.
  
### 2. Item-Item

  Thay vì xác định độ tương đồng giữa các user, chúng tôi sẽ xác định các item tương đồng. Từ đó đưa ra gợi ý cho user những item tương tự.


## Training and Test

  Chạy file TrainAndTestSplitting.py để chia tập dữ liệu thành 2 tập:
  - *Train (99%)* 
  - *Test (1%)*
  
  Và tỉ lệ các user trong 2 tập Train và Test cũng được chia theo tỉ lệ trên và sử dụng hàm `Root Mean Squared Error (RMSE)` để tính sai số.
  
  ![image](https://user-images.githubusercontent.com/105763597/210488064-cfa1062c-fd1e-4d09-87f5-0bb2e1758a87.png)

    Sau khi đánh giá kết quả 10 bộ Train, Test khác nhau:
  
  ![image](https://user-images.githubusercontent.com/104374448/210417568-2513c01b-f435-418d-aa46-d2f5d78f1cb0.png)
   
    Và kết quả thu được với *k* `(nearest- neaighbor)` lần lượt là `[1, 2, 5, 10, 15, 20, 30, 50, 100]`
  
  ![image](https://user-images.githubusercontent.com/104374448/210417218-476831f5-b63a-4ae7-8056-99ab055b269a.png)
  
   Dựa vào kết quả trên, ta có thể đánh giá tập dữ liệu phù hợp với hướng tiếp cận Item-Item hơn so với hướng tiếp cận User-User.

## Run 

  Yêu cầu hệ thống:
  - [Cài đặt python](https://www.python.org/downloads)
  - Cài đặt thư viện cần thiết: numpy`pip install numpy`, pandas`pip install pandas`, sklearn`pip install sklearn`, tkinter`pip install tkinter`, random`pip install random`, csv`pip install csv`
 
  Chạy chương trình:
  - [Clone git repository](https://github.com/NamAnhVH/SteamRecommendSystem.git) hoặc download zip.
  - Chạy file TrainAndTestSplitting.py`python TrainAndTestSplitting.py`
  - Chạy file gui.py`python gui.py`
  - Lựa chọn ListUser để hiện danh sách User sau đó lựa chọn user muốn được gợi ý

## Reference

  - [1] [Collaborative Filtering – Stanford University](https://www.youtube.com/watch?v=h9gpufJFF-0&t=436s)
  - [2] [Ekstrand, Michael D., John T. Riedl, and Joseph A. Konstan. “Collaborative filtering recommender systems” 22011]
  - [3] [Recomender System Tutorial](https://www.datacamp.com/tutorial/recommender-systems-python)


