from datetime import datetime
class Tabler:
    def __init__(self, title=None, show_date=False, rows=None, headers=None, row_paddings=None, row_alignments=None, header_alignments=None, wrap_text=True, max_length=32):
        self.title = title
        self.show_date = show_date
        self.rows = rows
        self.headers = headers or []
        self.row_paddings = row_paddings or [0] * len(rows[0])
        self.row_alignments = row_alignments or ['left'] * len(rows[0])
        self.header_alignments = header_alignments or ['left'] * len(headers[0])
        self.wrap_text = wrap_text
        self.max_length = max_length

        if not all(len(row) == len(rows[0]) for row in rows):
            raise ValueError("All rows must have the same number of columns")
        
    def _format_cell(self, content, width, alignment='left'):
        """Format a single cell with specified padding and alignment"""
        content = str(content)
        if alignment == 'left':
            return content.ljust(width)
        elif alignment == 'right':
            return content.rjust(width)
        elif alignment == 'center':
            return content.center(width)
        return content
    
    def create_table(self):
        if(self.wrap_text):
            self.rows = [
                [(cell[:self.max_length] + '...') if len(cell) > self.max_length else cell for cell in row]
                for row in self.rows
            ]

        widths = [
            max((len(str(row[i])) + pad for row in self.rows), default=0)
            for i, pad in enumerate(self.row_paddings)
        ]
        header_widths = [len(item) + pad for item, pad in zip(self.headers, self.row_paddings)]

        if self.headers:
            widths = [max(a, b) for a, b in zip(widths, header_widths)]
        
        total_width = sum(widths) + len(widths) + 1
        table_lines = []

        table_lines.append('┌' + '┬' * (total_width + 4) + '┐')
        table_lines.append('├' + '┴' * (total_width + 4) + '┤')
        
        if self.title or self.show_date:
            if self.title:
                table_lines.append(f'│{self.title.center(total_width + 4)}│')
            if self.show_date:
                date = datetime.now().strftime("%d/%m/%Y")
                table_lines.append(f'│{date.center(total_width + 4)}│')
        
        if self.headers:
            header_row = '│' + '│'.join(
                ' ' + self._format_cell(header, width, alignment) + ' ' 
                for header, width, alignment in zip(self.headers, widths, self.header_alignments)
            ) + '│'
            table_lines.append('├' + '┬'.join('─' * (width + 2) for width in widths) + '┤')
            table_lines.append(header_row)
        
        for i, row in enumerate(self.rows):
            if i == 0 and not self.headers:
                table_lines.append('├' + '┬'.join('─' * (width + 2) for width in widths) + '┤')
            else:
                table_lines.append('├' + '┼'.join('─' * (width + 2) for width in widths) + '┤')
            
            data_row = '│' + '│'.join(
                ' ' + self._format_cell(cell, width, alignment) + ' ' 
                for cell, width, alignment in zip(row, widths, self.row_alignments)
            ) + '│'
            table_lines.append(data_row)
        
        table_lines.append('└' + '┴'.join('─' * (width + 2) for width in widths) + '┘')
        
        return '\n'.join(table_lines)