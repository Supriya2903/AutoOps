pipeline {
    agent any

    triggers {
        githubPush()  // Trigger pipeline on GitHub push events
    }

    environment {
        PYTHON_PATH = "C:\\Users\\supri\\AppData\\Local\\Programs\\Python\\Python311"  // Adjusted to real Python location
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
                    docker.build('your-application-name')  // Build Docker image
                }
            }
        }

        stage('Monitor Jenkins Job Status') {
            steps {
                script {
                    // Run the Python script from the correct directory
                    withEnv(["PATH+PYTHON=${env.PYTHON_PATH}"]) {
                        sh '''
                            if command -v python3 > /dev/null; then
                                python3 AutoOps-SelfHealing/monitor_jenkins.py
                            else
                                python AutoOps-SelfHealing/monitor_jenkins.py
                            fi
                        '''
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

