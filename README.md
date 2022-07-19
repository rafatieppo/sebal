<body>
<h1 id="sebal-model-by-means-grass-and-python">SEBAL model by means GRASS and PYTHON</h1>
<p><a href="https://doi.org/10.5281/zenodo.1303413"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.1303413.svg" alt="DOI" /></a></p>
<h2 id="motivation">Motivation</h2>
<p>Now days it is noticed several occurrences about water shortage in agriculture, decreasing yield crops and profits. The irrigation system is a resource to aid the farmers to manage the system production to achieve a reasonable yield. Among several variables for a irrigation management, there are two of them with a major importance, the crop coefficient (kc) and Reference crop evapotranspiration (ETo) <span class="citation">(Gondim et al., 2005)</span>.</p>
<p>In the last decades the remote sensing techniques has been used to identify landscapes, soil classes, and water energy balance as well, providing conditions to analyze data in a regional scale. By means orbital sensors and algorithms to convert digital numbers to reflectance and radiation flux, remotesensing methods to predict the evapotranspiration is a important tool to handle the hydrological cycle <span class="citation">(Bernardo et al., 2006)</span>.</p>
<p>The SEBAL (Surface Energy Balance Algorithm for Land) uses the surface energy balance to predict some hydrological features (evapotranspiration, water deficit, etc) and Its main creator is Professor Wim G. M. Bastiaanssen <span class="citation">(Bastiaanssen et al., 1998)</span>. That method has been validated under several conditions for different locations (<span class="citation">(Bastiaanssen, 2000)</span>,<span class="citation">(Bastiaanssen et al., 2002)</span>, <span class="citation">(Santos et al., 2010)</span>).</p>
<p>There are several available algorithms to evapotranspiration prediction (<span class="citation">(Wolff, 2016)</span>, <span class="citation">(Cavalcante et al., 2016)</span>, <span class="citation">(Hessels et al., 2017)</span>). However is missing a specific code to run on python 3 and GRASS 74. Thus we aimed to implement SEBAL model for Landsat 8 iamges using the language Python version 3 <span class="citation">(Rossum, 1995)</span> and GRASS version 7.4 <span class="citation">(Neteler et al., 2012)</span>.</p>

<h2 id="running">How to run</h2>

You can read the post on:
<ul>
<li>[SEBAL model by means GRASS and PYTHON SEBAL](https://rafatieppo.github.io/post/2022_07_13_sebalpy_grass/)</li>
</ul>

You can find the video:
<ul>
<li>[Part1 - Pytyhon Environment and install packages](https://youtu.be/ffrZ6_VPxDQ)</li>
<li>[Part2 - Config and Run the script](https://youtu.be/z96M6DZ5noY)</li>
</ul

<h2 id="logs">Logs</h2>

<h3>Mon 2022-07-18 10:50:16 -04</h3>
<ul>
<li>The method to set GRASS GIS environment was changed, now in this script is not created a new `mapset`. In the script just is required to assign a existing `location` and `mapset`.</li>
<li>At line 92 was create a string variable `mdtrast_mapset`, it is to make easier the computation region assignement. It provides a condiotion to call MDTrast from any `mapset`.</li>
</ul>

<h2 id="notes">Notes</h2>
<ul>
<li>Tested on Ubuntu 18.04 LTS</li>
<li>Tested on DEBIAN 11</li>
</ul>
<h2 id="references" class="unnumbered">References</h2>
<div id="refs" class="references">
<div id="ref-BASTIAANSSEN2000">
<p>Bastiaanssen, W.G.M., 2000. SEBAL-based sensible and latent heat fluxes in the irrigated Gediz Basin, Turkey. Journal of Hydrology 229, 87–100. <a href="https://doi.org/https://doi.org/10.1016/S0022-1694(99)00202-4" class="uri">https://doi.org/https://doi.org/10.1016/S0022-1694(99)00202-4</a></p>
</div>
<div id="ref-BASTIAANSSEN2002AC">
<p>Bastiaanssen, W.G.M., Ahmad, M.-u.-D., Chemin, Y., 2002. Satellite surveillance of evaporative depletion across the Indus Basin. Water Resources Research 38, 9–1–9–9. <a href="https://doi.org/10.1029/2001WR000386" class="uri">https://doi.org/10.1029/2001WR000386</a></p>
</div>
<div id="ref-BASTIAANSSEN1998MFH">
<p>Bastiaanssen, W.G.M., Menenti, M., Feddes, R.A., Holtslag, A.A.M., 1998. A remote sensing surface energy balance algorithm for land (SEBAL). 1. Formulation. Journal of Hydrology 212-213, 198–212. <a href="https://doi.org/https://doi.org/10.1016/S0022-1694(98)00253-4" class="uri">https://doi.org/https://doi.org/10.1016/S0022-1694(98)00253-4</a></p>
</div>
<div id="ref-BERNARDO2006SM">
<p>Bernardo, S., Soares, A.A., Mantovani, E.C., 2006. Manual de irrigação, 8th ed. UFV, Viçosa.</p>
</div>
<div id="ref-CAVALCANTE2016IBJC">
<p>Cavalcante, L.B., Inácio, A. da S., Barros, H.G., Jiménez, Nicácio, R.M., Coelho, S.M.S. da C., 2016. Cálculo do saldo de radiação pelo algoritmo sebal na porção do baixo-médio São Francisco, Brasil, utilizando um software de código livre. Revista Brasileira de Cartografia 1515–1529.</p>
</div>
<div id="ref-GONDIM2005TB">
<p>Gondim, R., Teixeira, A.d.S., Barbosa, F., 2005. Novo paradigma para a água e coeficientes de cultivos aplicados à gestão de recursos hídricos em nível de bacia hidrográfica. Revista Item Irrigação e Tecnologia 14–18.</p>
</div>
<div id="ref-HESSELS2017OTB">
<p>Hessels, T., Opstal, J. van, Trambauer, P., Bastiaanssen, W., Smiej, M.F., Mohamed, Y., Er-Raji, A., 2017. pySEBAL_3.3.8.</p>
</div>
<div id="ref-GRASS2012NB">
<p>Neteler, M., Bowman, M.H., Landa, M., Metz, M., 2012. GRASS GIS: a multi-purpose Open Source GIS. Environmental Modelling &amp; Software 31, 124–130. <a href="https://doi.org/10.1016/j.envsoft.2011.11.014" class="uri">https://doi.org/10.1016/j.envsoft.2011.11.014</a></p>
</div>
<div id="ref-PYTHONR">
<p>Rossum, G. van, 1995. Python tutorial (No. CS-R9526). Centrum voor Wiskunde en Informatica (CWI), Amsterdam.</p>
</div>
<div id="ref-SANTOS210FA">
<p>Santos, T.V. dos, Fontana, D.C., Alves, R.C.M., 2010. Avaliação de fluxos de calor e evapotranspiração pelo modelo SEBAL com uso de dados do sensor ASTER. Pesquisa Agropecuária Brasileira 45, 488–496. <a href="https://doi.org/10.1590/S0100-204X2010000500008" class="uri">https://doi.org/10.1590/S0100-204X2010000500008</a></p>
</div>
<div id="ref-WOLF2016SEBAL">
<p>Wolff, W., 2016. wwolff7/SEBAL_GRASS. <a href="https://doi.org/10.5281/zenodo.167350" class="uri">https://doi.org/10.5281/zenodo.167350</a></p>
</div>
</div>
</body>
</html>
