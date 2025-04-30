pipeline {
    agent any

    triggers {
        githubPush()  // This will trigger the pipeline on GitHub push events
    }

    environment {
        PYTHON_PATH = "C:\\Users\\supri\\AppData\\Local\\Microsoft\\WindowsApps"
        PYTHON_HOME = '/usr/bin/python3'  // Adjust if needed
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/Supriya2903/AutoOps'  // Your GitHub repository
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean install'  // Maven build step
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'  // Run unit tests using Maven
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('your-application-name')  // Build Docker image using Maven
                }
            }
        }

        stage('Monitor Jenkins Job Status') {
            steps {
                script {
                    // Run the Python script that monitors Jenkins job status and retries on failure
                    withEnv(["PATH+PYTHON=${env.PYTHON_PATH}"]) {
                        sh 'python3 monitor_jenkins.py || python monitor_jenkins.py'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

