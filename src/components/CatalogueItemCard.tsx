import { Link } from 'react-router-dom'
import type { CatalogueItemType } from 'types/CatalogueItem.type'
import HOME_PATH from '../constants'

interface CatalogueItemProperties {
	catalogueItemData: CatalogueItemType
}

const CatalogueItemCard = ({ catalogueItemData }: CatalogueItemProperties) => {
	const {
		id,
		name,
		description,
		organization,
		'country-region': countryRegion,
		'date-added': dateAdded,
		'date-modified': dateModified,
		'year-period': yearPeriod,
		'card-type': cardType
	} = catalogueItemData

	let yearPeriodSection
	if (yearPeriod) {
		yearPeriodSection = <span> ({yearPeriod})</span>
	}

	let countryRegionSection
	if (countryRegion) {
		countryRegionSection = (
			<span className='w-1/2 text-xs text-gray-600'>
				Country/Region: {countryRegion}
			</span>
		)
	}

	let dateModifiedSection
	if (dateModified) {
		dateModifiedSection = (
			<span className='w-1/2 text-xs text-gray-600'>
				Date Updated: {dateModified}
			</span>
		)
	}

	return (
		<Link to={`${HOME_PATH}/catalogue/${id}`}>
			<div className='my-3 flex flex-col rounded p-3 hover:bg-gray-100 hover:duration-300'>
				<span className='text-xs text-gray-600'>{organization.name}</span>
				<div className='text-base font-semibold text-cloud-burst'>
					{name}
					{yearPeriodSection}
				</div>
				<p className='text-xs text-gray-600'>{description}</p>
				<div className='mt-3 flex flex-row'>
					{countryRegionSection}
					<span className='w-1/2 text-xs text-gray-600'>
						Date Created: {dateAdded}
					</span>
					{dateModifiedSection}
					<span className='w-1/2 text-xs text-gray-600'>Type: {cardType}</span>
				</div>
			</div>
		</Link>
	)
}

export default CatalogueItemCard