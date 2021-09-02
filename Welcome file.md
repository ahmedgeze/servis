---


---

<h1 id="case-document">Case Document</h1>
<p>In this project use maven and java 11.<br>
Project unit test in tests folder via JUNIT5.<br>
Database is mysql.</p>
<h1 id="case-details">Case Details</h1>
<ol>
<li>
<p>Installation<br>
This project has been Dockerize so if you want to run my application please run below commands.</p>
<blockquote>
<p>docker build -t springio/gs-spring-boot-docker .<br>
docker-compose up</p>
</blockquote>
<p>Application  run 8080 port on your localhost.</p>
</li>
<li>
<p>Testing<br>
Project has many unit test.Test coverage rates are 86% Class coverage, 54% Method coverage,64% line coverage.</p>
</li>
<li>
<p>Endpoints<br>
This project has 2 endpoints. Api context is <strong>/link-converter</strong> ,fist api endpoint  is <strong>/full-link</strong>   and second api endpoint is <strong>/deep-link</strong>.</p>

<table>
<thead>
<tr>
<th>Api Endpoint</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>link-converter/full-link</td>
<td>This api convert full link  from given input deep link</td>
</tr>
<tr>
<td>link-converter/deep-link</td>
<td>This api convert deep link  from given input full link</td>
</tr>
</tbody>
</table><p>Any other details listing swagger ui endpoint : <a href="http://localhost:8080/swagger-ui.html">http://localhost:8080/swagger-ui.html</a></p>
</li>
<li>
<p>Data Tables<br>
Main major table descriptions.</p>

<table>
<thead>
<tr>
<th>Table Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>api_log</td>
<td>This table contains main request body. This table contains request id ,request status,error code,endpoint,create date update date eg.</td>
</tr>
<tr>
<td>url</td>
<td>This table contains input or output of each request ,link type(full link deep link),which page(product,search,home page),path,raw url</td>
</tr>
<tr>
<td>url_query</td>
<td>This table contains each query parameter of url like key value</td>
</tr>
</tbody>
</table></li>
</ol>
<p>5.Used Additional Libraries<br>
-Mapstruct<br>
-Apache Commons<br>
-Open api ui<br>
-Lombok</p>

