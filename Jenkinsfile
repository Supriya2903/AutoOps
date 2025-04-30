pipeline{
    agent any
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
       
    }
}