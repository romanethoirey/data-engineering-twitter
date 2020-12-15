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
                        sh 'python unit_testing.py'
                    }
                }
            }
        }
        stage('Stress test'){
            steps{
                script{
                    if(env.BRANCH_NAME == 'develop')
                        sh 'locust -f stress_test.py &'
                        input 'Done with stress test ?'
                }
            }
        }
        stage('Release'){
            steps{
                script{
                    if(env.BRANCH_NAME == 'develop'){
                        sh 'git br -d release'
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
                        //sh 'git br -d main'
                        sh 'git co main'
                        sh 'git merge origin/release'
                        sh 'git pull origin main'
                        sh 'git push origin main'
                        sh 'git branch -D origin/release'
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
