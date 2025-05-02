<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:html="http://www.w3.org/1999/xhtml"
    exclude-result-prefixes="html">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/bibliotheque">
  <html>
    <head>
      <title>Liste des livres</title>
      <link rel="stylesheet" href="../static/style.css"/>
    </head>
    <body>
      <h2>Bibliothèque</h2>
      <input type="text" id="searchInput" onkeyup="filterBooks()" placeholder="Rechercher un livre..."/>
      
      <!-- Form to add books -->
      <form id="addForm" onsubmit="addBook(event)">
        <input type="text" id="titre" placeholder="Titre" required="required"/>
        <input type="text" id="auteur" placeholder="Auteur" required="required"/>
        <input type="number" id="annee" placeholder="Année" required="required"/>
        <input type="text" id="genre" placeholder="Genre" required="required"/>
        <select id="disponible">
          <option value="Disponible">Disponible</option>
          <option value="Indisponible">Indisponible</option>
        </select>
        <button type="submit">Ajouter</button>
      </form>
      
      <table id="bookTable">
        <tr>
          <th>Titre</th>
          <th>Auteur</th>
          <th>Année</th>
          <th>Genre</th>
          <th>Disponible</th>
          <th>Action</th>
        </tr>

        <xsl:for-each select="./livre">
          <tr>
            <td><xsl:value-of select="titre"/></td>
            <td><xsl:value-of select="auteur"/></td>
            <td><xsl:value-of select="annee"/></td>
            <td><xsl:value-of select="genre"/></td>
            <td><xsl:value-of select="disponible"/></td>
            <td>
              <button onclick="deleteRow(this)">Supprimer</button>
            </td>
          </tr>
        </xsl:for-each>
      </table>

      <script src="../static/script.js"></script>
    </body>
  </html>
</xsl:template>


</xsl:stylesheet>
