from flask import Blueprint, request, jsonify, send_file
from src.models.peca import db, Verificacao
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import qrcode
import io
import os
from datetime import datetime

etiqueta_bp = Blueprint('etiqueta', __name__)

def gerar_qr_code(texto):
    """Gera um QR code e retorna como bytes"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer

def criar_etiqueta_pdf(verificacao):
    """Cria uma etiqueta em PDF para a verificação"""
    buffer = io.BytesIO()
    
    # Configurações da página (tamanho de etiqueta)
    width = 100 * mm
    height = 70 * mm
    
    c = canvas.Canvas(buffer, pagesize=(width, height))
    
    # Cores
    cor_header = HexColor('#4f46e5')
    cor_texto = HexColor('#1e293b')
    cor_status_ok = HexColor('#10b981')
    cor_status_erro = HexColor('#dc2626')
    cor_status_warning = HexColor('#d97706')
    
    # Header
    c.setFillColor(cor_header)
    c.rect(0, height - 20*mm, width, 20*mm, fill=1)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    text_width = c.stringWidth("ETIQUETA DE VERIFICAÇÃO", "Helvetica-Bold", 12)
    c.drawString((width - text_width)/2, height - 10*mm, "ETIQUETA DE VERIFICAÇÃO")
    
    # Conteúdo principal
    y_pos = height - 30*mm
    
    # Nome da peça
    c.setFillColor(cor_texto)
    c.setFont("Helvetica-Bold", 16)
    text_width = c.stringWidth(verificacao.peca.nome, "Helvetica-Bold", 16)
    c.drawString((width - text_width)/2, y_pos, verificacao.peca.nome)
    y_pos -= 8*mm
    
    # Peso
    c.setFont("Helvetica", 10)
    peso_text = f"Peso: {verificacao.peso_medido} kg"
    text_width = c.stringWidth(peso_text, "Helvetica", 10)
    c.drawString((width - text_width)/2, y_pos, peso_text)
    y_pos -= 5*mm
    
    # Quantidade
    qtd_text = f"Quantidade calculada: {verificacao.quantidade_calculada} peças"
    text_width = c.stringWidth(qtd_text, "Helvetica", 10)
    c.drawString((width - text_width)/2, y_pos, qtd_text)
    y_pos -= 8*mm
    
    # Status
    if verificacao.status == 'OK':
        cor_status = cor_status_ok
    elif verificacao.status == 'FALTANDO':
        cor_status = cor_status_erro
    else:
        cor_status = cor_status_warning
    
    c.setFillColor(cor_status)
    c.roundRect(width/2 - 25*mm, y_pos - 3*mm, 50*mm, 6*mm, 3*mm, fill=1)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    status_text = {
        'OK': 'PESO CORRETO',
        'FALTANDO': 'FALTANDO PEÇAS',
        'SOBRANDO': 'PEÇAS EXTRAS'
    }
    status_display = status_text.get(verificacao.status, verificacao.status)
    text_width = c.stringWidth(status_display, "Helvetica-Bold", 10)
    c.drawString((width - text_width)/2, y_pos, status_display)
    y_pos -= 10*mm
    
    # Data e código
    c.setFillColor(cor_texto)
    c.setFont("Helvetica", 8)
    data_formatada = verificacao.data_verificacao.strftime("%d/%m/%Y %H:%M")
    text_width = c.stringWidth(data_formatada, "Helvetica", 8)
    c.drawString((width - text_width)/2, y_pos, data_formatada)
    y_pos -= 4*mm
    text_width = c.stringWidth(verificacao.codigo_verificacao, "Helvetica", 8)
    c.drawString((width - text_width)/2, y_pos, verificacao.codigo_verificacao)
    
    # QR Code (lado esquerdo inferior)
    qr_data = f"VER:{verificacao.codigo_verificacao}|PECA:{verificacao.peca.nome}|PESO:{verificacao.peso_medido}|STATUS:{verificacao.status}"
    qr_buffer = gerar_qr_code(qr_data)
    
    # Salvar QR code temporariamente
    temp_qr_path = f"/tmp/qr_{verificacao.codigo_verificacao}.png"
    with open(temp_qr_path, 'wb') as f:
        f.write(qr_buffer.getvalue())
    
    # Adicionar QR code ao PDF
    c.drawImage(temp_qr_path, 5*mm, 5*mm, 15*mm, 15*mm)
    
    # Linha para assinatura
    c.line(width/2 + 5*mm, 10*mm, width - 5*mm, 10*mm)
    c.setFont("Helvetica", 8)
    c.drawString(width/2 + 5*mm, 6*mm, "Assinatura")
    
    c.save()
    
    # Limpar arquivo temporário
    if os.path.exists(temp_qr_path):
        os.remove(temp_qr_path)
    
    buffer.seek(0)
    return buffer

@etiqueta_bp.route('/etiqueta/<codigo_verificacao>', methods=['GET'])
def gerar_etiqueta(codigo_verificacao):
    """Gera e retorna a etiqueta em PDF para uma verificação"""
    try:
        verificacao = Verificacao.query.filter_by(codigo_verificacao=codigo_verificacao).first_or_404()
        
        pdf_buffer = criar_etiqueta_pdf(verificacao)
        
        filename = f"etiqueta_{codigo_verificacao}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@etiqueta_bp.route('/etiqueta/preview/<codigo_verificacao>', methods=['GET'])
def preview_etiqueta(codigo_verificacao):
    """Retorna preview da etiqueta em PDF para visualização"""
    try:
        verificacao = Verificacao.query.filter_by(codigo_verificacao=codigo_verificacao).first_or_404()
        
        pdf_buffer = criar_etiqueta_pdf(verificacao)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

