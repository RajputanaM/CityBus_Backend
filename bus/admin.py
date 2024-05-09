from django.contrib import admin
from .models import BusStation, Bus, Profile, Ticket, OtpRecord, ChatRoom, Member, Message, AdminProfile, Conductor

from django.http import HttpResponse
import csv
import xlwt
import json
# for pdf generations
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle



from django.db.models import Count
from django.http import JsonResponse

class ConductorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bus', 'mobile', 'email')
    list_filter = ('name', 'bus__id')  # Filter by name and bus ID

    def export_conductors_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="conductors.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Mobile', 'Email', 'Bus'])
        for conductor in queryset:
            writer.writerow([conductor.name, conductor.mobile, conductor.email, conductor.bus.bus_number])
        return response

    export_conductors_to_csv.short_description = "Export selected conductors to CSV"
    
    def export_conductors_to_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="conductors.pdf"'

        # Create a PDF document
        pdf = SimpleDocTemplate(response, pagesize=letter)
        data = []

        # Define table header
        table_header = ['Name', 'Mobile', 'Email', 'Bus']
        data.append(table_header)

        # Populate table data
        for conductor in queryset:
            data.append([conductor.name, conductor.mobile, conductor.email, conductor.bus.bus_number])

        # Create table and add data
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        # Add table to PDF document
        pdf.build([table])

        return response

    export_conductors_to_pdf.short_description = "Export selected conductors to PDF"

    
    # Associate the custom actions with the admin class
    actions = ['export_conductors_to_csv', 'export_conductors_to_pdf']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email')
    list_filter = ('name', 'email')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'bus', 'number_of_tickets', 'booking_date_time', 'is_active')
    list_filter = ('user', 'is_active')

class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'source_station', 'destination_station', 'departure_time', 'arrival_time', 'price_per_ticket')
    list_filter = ('source_station', 'destination_station')

    # Custom admin action for exporting buses data to CSV
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="buses.csv"'
        writer = csv.writer(response)
        writer.writerow(['Bus Number', 'Source Station', 'Destination Station', 'Departure Time', 'Arrival Time', 'Price per Ticket'])
        for bus in queryset:
            writer.writerow([bus.bus_number, bus.source_station, bus.destination_station, bus.departure_time, bus.arrival_time, bus.price_per_ticket])
        return response
    export_to_csv.short_description = "Export selected buses to CSV"

    def export_buses_to_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="buses.pdf"'

        # Create a PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        data = []
        for bus in queryset:
            data.append([bus.bus_number, bus.source_station.name, bus.destination_station.name, bus.departure_time, bus.arrival_time, bus.price_per_ticket])

        # Create a table and style
        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)
        elements = [table]

        # Add table to the PDF document
        doc.build(elements)
        return response

    export_buses_to_pdf.short_description = "Export selected buses to PDF"
    
    actions = ['export_to_csv', 'export_buses_to_pdf']


admin.site.register(Bus, BusAdmin)  # Register with the custom admin class
admin.site.register(Profile, ProfileAdmin)  # Register with the custom admin class
admin.site.register(Ticket, TicketAdmin)
admin.site.register(BusStation)
admin.site.register(AdminProfile)
admin.site.register(Conductor, ConductorAdmin)
