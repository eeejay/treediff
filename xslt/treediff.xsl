<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/sidebyside">
  <html>
    <head>
      <link rel="stylesheet" type="text/css" href="treedif.css" />
      <script type="text/javascript" src="aria_list.js" />
      <title>An Experiment</title>
    </head>
    <body>
      <table border="1">
        <tr>
          <xsl:apply-templates/> 
        </tr>
      </table>
    </body>
  </html>
</xsl:template>

<xsl:template match="left">
  <td>
    <xsl:apply-templates/> 
  </td>
</xsl:template>

<xsl:template match="right">
  <td>
    <xsl:apply-templates/> 
  </td>
</xsl:template>

<xsl:template match="accessible">
  <li>
    [<xsl:value-of select="@name"/> | <xsl:value-of select="@role"/>]
    <xsl:if test="count(child::node())">
      <ul>
        <xsl:apply-templates/> 
      </ul>
    </xsl:if>
  </li>
</xsl:template>

</xsl:stylesheet>
