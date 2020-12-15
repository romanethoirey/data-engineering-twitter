pipeline {
    agent any
    stages {
        stage('Build Docker'){
            steps{
                script{
                    if(env.BRANCH_NAME != 'main'){
                        sh 'docker-compose up -d'
                    }
                }
            }
        }
        stage('Testing'){
            steps{
                script{
                    if(env.BRANCH_NAME.contains('feat')){
                        sh 'echo Tests "python test_app.py"'
                    }
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
                        sh 'git co -b release'
                        sh 'git push origin release'
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
                        sh 'git co main'
                        sh 'git merge release'
                        // sh 'git br -D release'
                    }
                }
            }
        }
        stage('Stop Containers'){
            steps{
                script{
                   if(env.BRANCH_NAME != 'main'){
                        sh 'docker-compose down'
                    } 
                }
            }
        }
    }
}
