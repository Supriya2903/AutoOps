pipeline{
    agent any

    triggers{
        githubPush()
    }

    stages{
        stage('Checkout Code'){
            steps{
                git 'https://github.com/Supriya2903/AutoOps'
            }
        }
        stage('Build'){
            steps{
                sh 'mvn clean install'
            }
        }
        stage('Test'){
            steps{
                sh 'mvn test'
            }
        }
        stage('Build Docker Image'){
            steps{
                script{
                    docker.build('your-application-name')
                }
            }
        }
       
    }
}