# Use a base image with OpenJDK 11
FROM openjdk:11-jdk-slim

# Set working directory inside container
WORKDIR /app

# Copy the JAR file into the container
COPY target/AutoOps-1.0-SNAPSHOT.jar /app/your-application.jar

# Run the JAR file
ENTRYPOINT ["java", "-jar", "/app/your-application.jar"]
