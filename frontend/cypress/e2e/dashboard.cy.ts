describe('Dashboard E2E Tests', () => {
  beforeEach(() => {
    // Visit the dashboard page
    cy.visit('/')
  })

  it('should load the dashboard', () => {
    cy.contains('Tech Trend Sentiment Analyst').should('be.visible')
  })

  it('should display filter bar', () => {
    cy.contains('Filters').should('be.visible')
    cy.get('select').should('have.length.at.least', 2) // Keyword and Source filters
  })

  it('should display summary cards', () => {
    cy.contains('Total Articles').should('be.visible')
    cy.contains('Average Sentiment').should('be.visible')
    cy.contains('Filtered Results').should('be.visible')
  })

  it('should allow filtering by keyword', () => {
    // Wait for keywords to load
    cy.wait(1000)
    
    // Select a keyword if available
    cy.get('select').first().then(($select) => {
      if ($select.find('option').length > 1) {
        cy.get('select').first().select(1)
        // Wait for data to load
        cy.wait(2000)
        cy.contains('Filtered Results').should('be.visible')
      }
    })
  })

  it('should allow quick date range selection', () => {
    cy.contains('Quick ranges:').should('be.visible')
    cy.contains('7 days').should('be.visible')
    cy.contains('30 days').should('be.visible')
    cy.contains('90 days').should('be.visible')
    
    // Click on 7 days button
    cy.contains('7 days').click()
    cy.wait(1000)
  })

  it('should display sentiment chart', () => {
    cy.wait(2000) // Wait for data to load
    cy.contains('Sentiment Trend').should('be.visible')
  })
})

