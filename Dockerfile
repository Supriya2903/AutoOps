# Use an official OpenJDK runtime as a parent image
FROM openjdk:11-jdk-slim

# Set the working directory in the container
WORKDIR /app

# Copy the compiled JAR file from the Maven target directory into the container
COPY target/your-application.jar /app/your-application.jar

# Run the application
ENTRYPOINT ["java", "-jar", "your-application.jar"]
