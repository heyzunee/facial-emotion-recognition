# face-emotion-recognition
docker build -t emotion:v6 .

docker run -it -p 9000:9000 --name emotion_container emotion:v6

curl -X POST http://localhost:9000/emotion   
    -H "Content-Type: multipart/form-data"   
    -F "image=@/your_path/src/datasets/test/3.jpg"
