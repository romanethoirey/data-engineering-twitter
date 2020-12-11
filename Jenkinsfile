pipeline {
    agent any
    stages {
        stage('Build Docker'){
            steps{
                sh 'docker build -d -t twitter_app .'
            }
        }
        stage('Run Docker'){
            steps{
                sh 'docker run -p 5000:5000 -d --name twitter_app_c twitter_app'
            }
        }
        stage('Testing'){
            steps{
                sh 'echo Tests "python test_app.py"'
            }
        }
        stage('Stop Containers'){
            steps{
                sh 'docker rm -f twitter_app_c'
                sh 'docker rmi -f twitter_app'
            }
        }
    }
}
