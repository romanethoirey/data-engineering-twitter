pipeline {
    agent any
    stages {
        stage('Build Docker'){
            steps{
                script{
                    if(env.BRANCH_NAME != 'master'){
                        sh 'docker-compose up -d'
                    }
                }
            }
        }
        stage('Testing'){
            steps{
                script{
                    if(env.BRANCH_NAME == 'feat')
                        sh 'echo Tests "python test_app.py"'
                }
            }
        }
        stage('Stress test'){
            steps{
                script{
                    if(env.BRANCH_NAME == 'develop')
                        sh 'echo Stress the tests'
                }
            }
        }
        stage('Release'){
            steps{
                script{
                    if(env.BRANCH_NAME == 'develop'){
                        echo 'git co -b release'
                    }
                }
            }
        }
        stage('Acceptance Test'){
            steps{
                script{
                    if(env.BRANCH_NAME == 'release'){
                        input 'Proceed with live deploy ?'
                    }
                }
            }
        }
        stage('Merge to master'){
            steps{
                script{
                    if(env.BRANCH_NAME == 'release'){
                        sh 'git merge master'
                    }
                }
            }
        }
        stage('Stop Containers'){
            steps{
                script{
                   if(env.BRANCH_NAME != 'master'){
                        sh 'docker-compose down'
                    } 
                }
            }
        }
    }
}
