FROM tomcat:9.0-alpine

LABEL version = "1.1.1"
COPY target/petclinic.war /usr/local/tomcat/webapps/petclinic.war
