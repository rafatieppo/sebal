<body>
<h1 id="sebal-model-by-means-grass-and-python">SEBAL model by means GRASS and PYTHON</h1>
<h2 id="motivation">Motivation</h2>
<p>Now days it is noticed several occurrences about water shortage in agriculture, decreasing yield crops and profits. The irrigation system is a resource to aid the farmers to manage the system production to achieve a reasonable yield. Among several variables for a irrigation management, there are two of them with a major importance, the crop coefficient (kc) and Reference crop evapotranspiration (ETo) <span class="citation">(Gondim, Teixeira, and Barbosa 2005)</span>.</p>
<p>In the last decades the remote sensing techniques has been used to identify landscapes, soil classes, and water energy balance as well, providing conditions to analyze data in a regional scale. By means orbital sensors and algorithms to convert digital numbers to reflectance and radiation flux, remotesensing methods to predict the evapotranspiration is a important tool to handle the hydrological cycle <span class="citation">(Bernardo, Soares, and Mantovani 2006)</span>.</p>
<p>The SEBAL (Surface Energy Balance Algorithm for Land) uses the surface energy balance to predict some hydrological features (evapotranspiration, water deficit, etc) and Its main creator is Professor Wim G. M. Bastiaanssen <span class="citation">(W G M Bastiaanssen et al. 1998)</span>. That method has been validated under several conditions for different locations (<span class="citation">(W G M Bastiaanssen 2000)</span>,<span class="citation">(Wim G. M. Bastiaanssen, Ahmad, and Chemin 2002)</span>, <span class="citation">(Santos, Fontana, and Alves 2010)</span>).</p>
<p>There are several available algorithms to evapotranspiration prediction (<span class="citation">(Wolff 2016)</span>, <span class="citation">(Cavalcante et al. 2016)</span>, <span class="citation">(Hessels et al. 2017)</span>). However is missing a specific code to run on python 3 and GRASS 74. Thus we aimed to implement SEBAL model for Landsat 8 iamges using the language Python version 3 <span class="citation">(Rossum 1995)</span> and GRASS version 7.4 <span class="citation">(Neteler et al. 2012)</span>.</p>
<h2 id="requirements">Requirements</h2>
<ul>
<li><a href="https://grass.osgeo.org/#">GRASS GIS version 7.4</a>
<ul>
<li>GRASS GUI</li>
<li>GRASS DEV</li>
</ul></li>
<li>Python 3.x, sugestion: <a href="https://anaconda.org/anaconda/python">CONDA</a></li>
</ul>
<p>Make sure your system has Python Libraries:</p>
<ul>
<li>math</li>
<li>numpy</li>
<li>os</li>
<li>grass_session</li>
<li>grass.script</li>
<li>osgeo</li>
</ul>
<h2 id="how-to-use">How to use</h2>
<ol style="list-style-type: decimal">
<li>Download at Landsat 8 images (LS8 - OLI/TIRS)</li>
<li>Reproject all the images (LS8 images) for the interested coordinate reference system (e.g. EPSG:32721)</li>
<li>For all images remove null values</li>
<li>Get Digital Elevation Model (DEM) from ASTER</li>
<li>You must reproject the DEM file for the same coordinate reference system of interest, rename it as <strong>MDT_Sebal.TIF</strong></li>
<li>Create a <em>GRASS</em> Session with GRASS-GIS software. You need to assign <em>GRASS location</em> and <em>GRASS Mapset</em>. Note that all maps must have the same coordinate reference system (projection). For further information about <em>GRASS</em> you can check <a href="https://grass.osgeo.org/">GRASS-GIS</a>.</li>
<li>Make sure that all files are in the same folder, <code>SEBAL_v10.py</code> inclusive.</li>
<li>Launch a text editor file and open <code>SEBAL_v10.py</code>. Find the lines <strong>67, 68, 69</strong>, you will find:</li>
</ol>
<pre><code>PERMANENT.open(gisdb=&#39;/home/rafatieppo/Documents/QGIS_SEBAL/20170904/&#39;,
               location=&#39;sirgas2000utm21s&#39;,
               create_opts=&#39;EPSG:31981&#39;)</code></pre>
<p>Replace the text between quotes, e.g.:</p>
<pre><code>PERMANENT.open(gisdb=&#39;path for YOUR files&#39;,
               location=&#39;YOUR folder location&#39;,
               create_opts=&#39;YOUR reference coordinate system&#39;)</code></pre>
<p>after that, save and close it.</p>
<ol start="10" style="list-style-type: decimal">
<li>If use Linux launch the <em>Terminal</em>, or if are Windows user launch <em>DOS Prompt</em>. Once you are in correct folder (that one with all your files) just run <code>python SEBAL_v10.py</code>, and insert the required values.</li>
</ol>
<h2 id="notes">Notes</h2>
<p>Tested on Ubuntu 16.04 LTS</p>
<h2 id="references">References</h2>
<?xml version="1.0" encoding="utf-8"?>

<div id="refs" class="references">
<div id="ref-BASTIAANSSEN2000">
<p>Bastiaanssen, W G M. 2000. “SEBAL-based sensible and latent heat fluxes in the irrigated Gediz Basin, Turkey.” <em>Journal of Hydrology</em> 229 (1): 87–100. doi:<a href="https://doi.org/https://doi.org/10.1016/S0022-1694(99)00202-4">https://doi.org/10.1016/S0022-1694(99)00202-4</a>.</p>
</div>
<div id="ref-BASTIAANSSEN1998MFH">
<p>Bastiaanssen, W G M, M Menenti, R A Feddes, and A A M Holtslag. 1998. “A remote sensing surface energy balance algorithm for land (SEBAL). 1. Formulation.” <em>Journal of Hydrology</em> 212-213: 198–212. doi:<a href="https://doi.org/https://doi.org/10.1016/S0022-1694(98)00253-4">https://doi.org/10.1016/S0022-1694(98)00253-4</a>.</p>
</div>
<div id="ref-BASTIAANSSEN2002AC">
<p>Bastiaanssen, Wim G. M., Mobin-ud-Din Ahmad, and Yann Chemin. 2002. “Satellite surveillance of evaporative depletion across the Indus Basin.” <em>Water Resources Research</em> 38 (12): 9–1–9–9. doi:<a href="https://doi.org/10.1029/2001WR000386">10.1029/2001WR000386</a>.</p>
</div>
<div id="ref-BERNARDO2006SM">
<p>Bernardo, Salassier, Antonio Alves Soares, and Everardo Chartuni Mantovani. 2006. <em>Manual de irrigação</em>. 8th ed. Viçosa: UFV.</p>
</div>
<div id="ref-CAVALCANTE2016IBJC">
<p>Cavalcante, Lucas Barbosa, Aline da Silva Inácio, Heliofábio Gomes Barros, Jiménez, Rosilene Mendonça Nicácio, and Simone Marilene Sievert da Costa Coelho. 2016. “Cálculo do saldo de radiação pelo algoritmo sebal na porção do baixo-médio São Francisco, Brasil, utilizando um software de código livre.” <em>Revista Brasileira de Cartografia</em>, no. 68: 1515–29.</p>
</div>
<div id="ref-GONDIM2005TB">
<p>Gondim, R., A. d. S. Teixeira, and F. Barbosa. 2005. “Novo paradigma para a água e coeficientes de cultivos aplicados à gestão de recursos hídricos em nível de bacia hidrográfica.” <em>Revista Item Irrigação E Tecnologia</em>, no. 67: 14–18.</p>
</div>
<div id="ref-HESSELS2017OTB">
<p>Hessels, Tim, Jonna van Opstal, Patricia Trambauer, Wim Bastiaanssen, Mohamed Faouzi Smiej, Yasir Mohamed, and Ahmed Er-Raji. 2017. “pySEBAL_3.3.8.” <a href="https://github.com/wateraccounting/SEBAL/blob/master/pySEBAL/pySEBAL{\_}code.py" class="uri">https://github.com/wateraccounting/SEBAL/blob/master/pySEBAL/pySEBAL{\_}code.py</a>.</p>
</div>
<div id="ref-GRASS2012NB">
<p>Neteler, M, M H Bowman, M Landa, and M Metz. 2012. “GRASS GIS: a multi-purpose Open Source GIS.” <em>Environmental Modelling &amp; Software</em> 31. Elsevier: 124–30. doi:<a href="https://doi.org/10.1016/j.envsoft.2011.11.014">10.1016/j.envsoft.2011.11.014</a>.</p>
</div>
<div id="ref-PYTHONR">
<p>Rossum, G van. 1995. “Python tutorial.” CS-R9526. Amsterdam: Centrum voor Wiskunde en Informatica (CWI).</p>
</div>
<div id="ref-SANTOS210FA">
<p>Santos, Thiago Veloso dos, Denise Cybis Fontana, and Rita Cássia Marques Alves. 2010. “Avaliação de fluxos de calor e evapotranspiração pelo modelo SEBAL com uso de dados do sensor ASTER.” <em>Pesquisa Agropecuária Brasileira</em> 45 (5). scielo: 488–96. doi:<a href="https://doi.org/10.1590/S0100-204X2010000500008">10.1590/S0100-204X2010000500008</a>.</p>
</div>
<div id="ref-WOLF2016SEBAL">
<p>Wolff, Wagner. 2016. “wwolff7/SEBAL_GRASS.” doi:<a href="https://doi.org/10.5281/zenodo.167350">10.5281/zenodo.167350</a>.</p>
</div>
</div>
</body>
</html>
